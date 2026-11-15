// Motor gráfico del tiempo profundo (de la acreción a 7 Ma). Pinta en la GPU, con un único sombreador de fragmentos,
// la textura Mercator que MapLibre proyecta sobre el globo o el plano: océanos con plataformas y fosas, relieve con
// sombreado, cinturones climáticos por latitud, mantos de hielo y banquisa, y magma animado. La geometría (costas
// fechadas, extensión de los hielos, colores de escena) sigue viniendo de los datos del atlas: aquí solo cambia el acabado.
// Si WebGL2 no está disponible se usa el pintor por CPU anterior (deep-surface.ts).
import type { FeatureCollection, Position } from 'geojson';
import { deepIceAt, type DeepScene } from './deep-earth';
import { drawDeepSurface as drawCpu } from './deep-surface';

const VERT = `#version 300 es
in vec2 aPos; out vec2 vUv;
void main(){ vUv = aPos*.5+.5; gl_Position = vec4(aPos,0.,1.); }`;

const FRAG = `#version 300 es
precision highp float;
in vec2 vUv; out vec4 outColor;
uniform sampler2D uM0, uM1, uM2;
uniform float uHasMask, uLandFrac, uTime, uAge, uProgress, uVeg, uOxid, uCold, uFerr, uHaze, uLush;
uniform int uMode, uIce;
uniform vec3 uOcean, uLand;
const float PI = 3.14159265359;

// --- Ruido símplex 3D (Ian McEwan, Ashima Arts; licencia MIT) ---
vec3 mod289(vec3 x){return x-floor(x*(1./289.))*289.;} vec4 mod289(vec4 x){return x-floor(x*(1./289.))*289.;}
vec4 permute(vec4 x){return mod289(((x*34.)+1.)*x);} vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-.85373472095314*r;}
float snoise(vec3 v){
  const vec2 C=vec2(1./6.,1./3.); const vec4 D=vec4(0.,.5,1.,2.);
  vec3 i=floor(v+dot(v,C.yyy)); vec3 x0=v-i+dot(i,C.xxx);
  vec3 g=step(x0.yzx,x0.xyz); vec3 l=1.-g; vec3 i1=min(g.xyz,l.zxy); vec3 i2=max(g.xyz,l.zxy);
  vec3 x1=x0-i1+C.xxx; vec3 x2=x0-i2+C.yyy; vec3 x3=x0-D.yyy;
  i=mod289(i);
  vec4 p=permute(permute(permute(i.z+vec4(0.,i1.z,i2.z,1.))+i.y+vec4(0.,i1.y,i2.y,1.))+i.x+vec4(0.,i1.x,i2.x,1.));
  float n_=.142857142857; vec3 ns=n_*D.wyz-D.xzx;
  vec4 j=p-49.*floor(p*ns.z*ns.z); vec4 x_=floor(j*ns.z); vec4 y_=floor(j-7.*x_);
  vec4 x=x_*ns.x+ns.yyyy; vec4 y=y_*ns.x+ns.yyyy; vec4 h=1.-abs(x)-abs(y);
  vec4 b0=vec4(x.xy,y.xy); vec4 b1=vec4(x.zw,y.zw);
  vec4 s0=floor(b0)*2.+1.; vec4 s1=floor(b1)*2.+1.; vec4 sh=-step(h,vec4(0.));
  vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy; vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;
  vec3 p0=vec3(a0.xy,h.x); vec3 p1=vec3(a0.zw,h.y); vec3 p2=vec3(a1.xy,h.z); vec3 p3=vec3(a1.zw,h.w);
  vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
  p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;
  vec4 m=max(.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.); m=m*m;
  return 42.*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
}
float fbm(vec3 p,int oct){float a=.5,s=0.,n=0.;for(int i=0;i<8;i++){if(i>=oct)break;s+=a*snoise(p);n+=a;p=p*2.03+vec3(17.1,-9.3,5.7);a*=.5;}return s/n;}
float ridged(vec3 p,int oct){float a=.5,s=0.,n=0.,w=1.;for(int i=0;i<8;i++){if(i>=oct)break;float r=1.-abs(snoise(p));r*=r;s+=a*r*w;n+=a;w=clamp(r*1.6,0.,1.);p=p*2.07+vec3(-3.7,11.9,7.3);a*=.5;}return s/n;}
vec3 hash3(vec3 p){p=vec3(dot(p,vec3(127.1,311.7,74.7)),dot(p,vec3(269.5,183.3,246.1)),dot(p,vec3(113.5,271.9,124.6)));return fract(sin(p)*43758.5453123);}
// Celdas de Voronói: x = distancia al borde entre celdas, y = identificador de celda.
vec2 voronoi(vec3 x){
  vec3 n=floor(x),f=fract(x); float d1=8.,d2=8.,id=0.;
  for(int k=-1;k<=1;k++)for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){
    vec3 g=vec3(float(i),float(j),float(k)); vec3 o=hash3(n+g); vec3 r=g+o-f; float d=dot(r,r);
    if(d<d1){d2=d1;d1=d;id=o.x+o.y*7.+o.z*13.;}else if(d<d2){d2=d;}
  }
  return vec2(sqrt(d2)-sqrt(d1),id);
}

float relief(vec3 P,float interior){
  float belts=pow(1.-abs(snoise(P*1.7+3.1)),5.);
  float margin=smoothstep(.15,.5,interior)*(1.-smoothstep(.55,.95,interior));
  float cord=pow(1.-abs(snoise(P*2.6-5.3)),3.5)*margin;
  float chain=clamp(belts*mix(1.,.5,interior)+cord*.9,0.,1.);
  float peaks=ridged(P*8.5,5);
  float hills=fbm(P*4.3+11.,5)*.5+.5;
  return hills*.16+fbm(P*19.,3)*.025+chain*(.3+.95*peaks)+peaks*.06;
}
vec3 blackbody(float t){
  vec3 c=mix(vec3(.05,.012,.01),vec3(.42,.035,.008),smoothstep(0.,.28,t));
  c=mix(c,vec3(.95,.27,.02),smoothstep(.22,.55,t));
  c=mix(c,vec3(1.,.72,.2),smoothstep(.5,.8,t));
  return mix(c,vec3(1.,.96,.78),smoothstep(.78,1.,t));
}

void main(){
  float merc=PI*(2.*vUv.y-1.);
  float lat=atan(sinh(merc)), lon=PI*(2.*vUv.x-1.);
  float cl=cos(lat);
  vec3 P=vec3(cl*cos(lon),cl*sin(lon),sin(lat));
  float alat=abs(lat)*57.29578+fbm(P*2.4+5.,3)*9.;
  vec3 east=normalize(vec3(-P.y,P.x,1e-6)), north=cross(P,east);
  vec3 col;

  if(uMode==1||uMode==2){
    // --- Océano de magma y corteza en enfriamiento ---
    float t=uTime*.035;
    vec3 w=vec3(fbm(P*1.6+vec3(0.,0.,t),4),fbm(P*1.6+vec3(5.2,1.3,-t),4),fbm(P*1.6+vec3(-3.1,8.4,t*.7),4));
    vec3 q=P*2.2+w*.9;
    float heat=fbm(q*1.5+vec3(t*.6,0.,-t*.4),6)*.5+.5;
    float fine=fbm(q*9.+t,4)*.5+.5;
    vec2 vc=voronoi(q*(uMode==1?3.2:5.5)+w*.6);
    float crack=1.-smoothstep(0.,uMode==1?.16:.07,vc.x);
    float pulse=.5+.5*sin(uTime*.7+vc.y*6.283+heat*9.);
    if(uMode==1){
      float crust=smoothstep(.5,.72,heat+fine*.18-uProgress*.06);        // balsas de corteza oscura a la deriva
      float temp=mix(.52+.42*heat+.1*fine,.1+.14*fine,crust);
      temp=max(temp,crack*(.72+.25*pulse));
      temp+=.07*pulse*(1.-crust);
      // Impactos de la acreción: destellos breves y dispersos.
      vec3 cell=floor(P*6.); vec3 hh=hash3(cell+floor(uTime*.12+hash3(cell).x*40.));
      float flash=smoothstep(.985,1.,hh.x)*exp(-10.*fract(uTime*.12+hash3(cell).x*40.))*smoothstep(.45,0.,length(fract(P*6.)-.5));
      col=blackbody(clamp(temp,0.,1.))+vec3(1.,.9,.7)*flash*1.5;
    }else{
      float lakes=smoothstep(.78-.2*uProgress,.95-.2*uProgress,heat+fine*.15);     // últimos lagos de lava
      float glow=crack*(.25+.6*uProgress)*(.55+.45*pulse)*(.6+.4*heat);
      float h0=fbm(q*6.,5), hx=fbm((q+east*.02)*6.,5), hy=fbm((q+north*.02)*6.,5);
      float shade=clamp(.5+(hx-h0)*3.-(hy-h0)*3.,0.,1.);
      vec3 crust=mix(vec3(.055,.05,.058),vec3(.2,.17,.165),shade*(.55+.45*fine));
      crust=mix(crust,vec3(.3,.25,.23),smoothstep(.55,.9,fine)*.25);
      col=crust+blackbody(clamp(max(glow,lakes*(.6+.3*pulse)),0.,1.))*smoothstep(.02,.3,max(glow,lakes));
    }
    outColor=vec4(clamp(col,0.,1.),1.); return;
  }

  // --- Tierra y océano ---
  float land,near,far;
  vec2 jit=vec2(snoise(P*34.),snoise(P*34.+9.1))*.0011;
  if(uHasMask>.5){
    land=smoothstep(.4,.6,texture(uM0,vUv+jit).r);
    vec2 e1=vec2(1./256.,0.), e2=vec2(1./64.,0.);
    near=(texture(uM1,vUv).r*2.+texture(uM1,vUv+e1).r+texture(uM1,vUv-e1).r+texture(uM1,vUv+e1.yx).r+texture(uM1,vUv-e1.yx).r)/6.;
    far=(texture(uM2,vUv).r*2.+texture(uM2,vUv+e2).r+texture(uM2,vUv-e2).r+texture(uM2,vUv+e2.yx).r+texture(uM2,vUv-e2.yx).r)/6.;
  }else{
    float n=fbm(P*1.25+vec3(4.2,-1.7,2.9),6)+fbm(P*11.,3)*.035;
    float th=.56-1.4*uLandFrac;
    land=smoothstep(th-.01,th+.01,n); near=smoothstep(th-.1,th+.1,n); far=smoothstep(th-.28,th+.3,n);
  }
  float interior=smoothstep(.5,.98,far);
  float h=relief(P,interior), e=.004;
  float hx=relief(P+east*e,interior), hy=relief(P+north*e,interior);
  vec3 nrm=normalize(vec3(-(hx-h)/e*.06,-(hy-h)/e*.06,1.));
  float shade=clamp(dot(nrm,normalize(vec3(-.55,.6,.58))),0.,1.);
  float macro=fbm(P*2.3+7.7,4);

  // Clima por latitud: cinturón ecuatorial húmedo, desiertos subtropicales, templado y polar.
  float tropic=exp(-pow(alat/11.,2.)), desert=exp(-pow((alat-25.)/10.,2.));
  float moist=clamp(.52+.5*tropic-.7*desert-.42*interior+.38*macro+.16*(1.-interior)+.25*uLush*(1.-desert),0.,1.);
  float coldLat=pow(alat/90.,2.2)*uCold;
  float vegLocal=smoothstep(0.,.32,moist-(1.-uVeg)*.95)*step(.001,uVeg)*(1.-smoothstep(.75,1.15,h));

  vec3 rockOld=mix(vec3(.2,.19,.19),vec3(.5,.46,.42),smoothstep(-.3,.5,macro+fbm(P*9.,3)*.4));
  vec3 rockRed=mix(vec3(.6,.33,.21),vec3(.78,.6,.4),smoothstep(-.4,.5,fbm(P*3.7-2.,4)+desert*.3));
  rockRed=mix(rockRed,vec3(.33,.27,.25),smoothstep(.35,.7,fbm(P*4.4+21.,3))*.6);
  vec3 barren=mix(rockOld,rockRed,uOxid);
  barren=mix(barren,vec3(.47,.43,.4),smoothstep(.6,1.2,h)*.7);
  vec3 forest=mix(vec3(.19,.32,.17),vec3(.08,.24,.12),tropic);
  forest=mix(forest,vec3(.16,.27,.2),smoothstep(45.,70.,alat));
  vec3 grass=mix(vec3(.52,.53,.27),vec3(.37,.46,.22),smoothstep(.35,.7,moist));
  vec3 green=mix(grass,forest,smoothstep(.45,.8,moist+fbm(P*14.,3)*.12));
  green=mix(green,vec3(.43,.42,.33),smoothstep(.55,.9,coldLat));                    // tundra
  vec3 landCol=mix(barren,green,vegLocal);
  landCol=mix(landCol,uLand,.2);
  landCol*=.5+.72*shade;
  landCol*=1.-.25*smoothstep(.0,.6,fbm(P*23.,3))*(1.-vegLocal)*.5;
  float snow=smoothstep(0.,.14,h*.85+coldLat*1.25-1.02+fbm(P*16.,3)*.06);
  landCol=mix(landCol,vec3(.93,.95,.97)*(.72+.34*shade),snow);
  // Volcanismo de la Tierra primitiva: focos incandescentes en las islas del Hádico y del Eoarcaico.
  float vents=smoothstep(.62,.8,snoise(P*19.+2.))*smoothstep(3500.,4100.,uAge);
  landCol+=blackbody(.55+.3*sin(uTime*.9+P.x*40.))*vents*.8;

  // Océano: fosas oscuras, plataformas claras y bajíos turquesa junto a la costa.
  float shelf=near*(1.-land);
  vec3 deep=uOcean*vec3(.42,.55,.72);
  vec3 mid=uOcean*vec3(.86,.95,1.02);
  vec3 shallow=mix(uOcean,vec3(.3,.74,.74),.5)+.06;
  vec3 sea=mix(deep,mid,smoothstep(0.,.3,far*.55+shelf*.9+macro*.12+.12));
  sea=mix(sea,shallow,smoothstep(.22,.62,shelf));
  sea*=.93+.1*fbm(P*6.+vec3(0.,0.,3.),4)+.035*fbm(P*42.,3);
  sea*=1.-.16*smoothstep(.1,.6,fbm(P*1.9+13.,5))*(1.-smoothstep(0.,.3,far));

  col=mix(sea,landCol,land);
  col=mix(col,mix(shallow,landCol,.55),(1.-abs(land*2.-1.))*.35);                    // orla costera

  // --- Hielo ---
  if(uIce>0){
    float rug=fbm(P*4.+1.3,5)*.17+fbm(P*13.,2)*.02;
    float cap=0.;
    if(uIce==1)cap=1.;
    else if(uIce==2)cap=(-P.z-.52+rug)*4.*mix(.22,1.,land);
    else if(uIce==3)cap=(-P.z-.86+rug)*8.;
    else if(uIce==4)cap=(abs(P.z)-.57+rug)*3.;
    else cap=land*smoothstep(.1,.45,fbm(P*3.1+2.,4)+h*.5)*smoothstep(-.1,.3,fbm(P*8.,3))*.8;
    cap=clamp(cap,0.,1.);
    if(cap>0.){
      vec2 floe=voronoi(P*24.+fbm(P*6.,3)*1.2);
      vec2 plate=voronoi(P*9.+fbm(P*3.,3)*.8);
      float dome=clamp(.55+.5*shade+.12*fbm(P*26.,3),0.,1.2);
      vec3 sheet=mix(vec3(.66,.8,.92),vec3(.96,.975,.99),smoothstep(.05,.7,cap))*(.68+.34*dome);
      sheet=mix(sheet,vec3(.5,.68,.84),(1.-smoothstep(0.,.09,abs(snoise(P*31.)*.5)))*.22*smoothstep(.2,.8,h));   // grietas
      float lead=smoothstep(0.,.07,floe.x);
      vec3 pack=mix(vec3(.74,.84,.91),vec3(.93,.955,.975),clamp(.5+floe.y*.07+fbm(P*30.,2)*.4,0.,1.));
      float packA=smoothstep(.02,.4,cap)*mix(lead,1.,smoothstep(.45,.95,cap));
      vec3 seaIce=mix(sea*.8,pack,packA);
      float landA=smoothstep(0.,.3,cap);
      vec3 landIce=mix(landCol,sheet,landA);
      if(uIce==1){
        // Tierra bola de nieve: hielo desnudo y azulado en los trópicos, nieve en latitudes medias y altas, y fracturas.
        float bare=1.-smoothstep(8.,34.,alat+fbm(P*3.,3)*14.);
        vec3 glacier=mix(vec3(.9,.94,.97),vec3(.5,.74,.87),bare*.85);
        glacier*=.88+.14*fbm(P*12.+vec3(0.,0.,5.),4);
        float fracture=1.-smoothstep(0.,.035,plate.x);
        glacier=mix(glacier,vec3(.2,.42,.56),fracture*.75);
        glacier=mix(glacier,vec3(.36,.6,.75),(1.-smoothstep(0.,.06,floe.x))*.25*bare);
        seaIce=glacier;
        landIce=mix(vec3(.82,.88,.93),vec3(.97,.98,.99),.5+.5*fbm(P*7.,3))*(.66+.38*shade);
        landIce=mix(landIce,vec3(.42,.36,.33)*(.6+.5*shade),smoothstep(.95,1.3,h)*.55);  // nunataks
      }
      col=mix(seaIce,landIce,land);
    }
  }

  // Calima anaranjada del Arcaico tardío y variante ferruginosa del océano (se conservan del atlas).
  col=mix(col,vec3(.68,.4,.2)*(.8+.4*dot(col,vec3(.33))),uHaze);
  col=mix(col,vec3(.62,.24,.145)*(.75+.5*dot(col,vec3(.33))),uFerr*(1.-land));
  col=mix(vec3(dot(col,vec3(.299,.587,.114))),col,1.08);
  outColor=vec4(clamp(col,0.,1.),1.);
}`;

interface Engine { gl: WebGL2RenderingContext; program: WebGLProgram; uniforms: Record<string, WebGLUniformLocation | null>; textures: WebGLTexture[]; masks: HTMLCanvasElement[] }
const engines = new WeakMap<HTMLCanvasElement, Engine | null>();
const rgb = (hex: string) => [parseInt(hex.slice(1, 3), 16) / 255, parseInt(hex.slice(3, 5), 16) / 255, parseInt(hex.slice(5, 7), 16) / 255];
const UNIFORMS = ['uM0', 'uM1', 'uM2', 'uHasMask', 'uLandFrac', 'uTime', 'uAge', 'uProgress', 'uVeg', 'uOxid', 'uCold', 'uFerr', 'uHaze', 'uLush', 'uMode', 'uIce', 'uOcean', 'uLand'];
const ICE: Record<string, number> = { snowball: 1, gondwana: 2, antarctic: 3, huronian: 4 };

function createEngine(canvas: HTMLCanvasElement): Engine | null {
  const gl = canvas.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false, alpha: false, powerPreference: 'high-performance' });
  if (!gl) return null;
  const compile = (type: number, src: string) => { const s = gl.createShader(type)!; gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s) ?? 'shader'); return s; };
  try {
    const program = gl.createProgram()!;
    gl.attachShader(program, compile(gl.VERTEX_SHADER, VERT)); gl.attachShader(program, compile(gl.FRAGMENT_SHADER, FRAG)); gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program) ?? 'link');
    const buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buffer); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(program, 'aPos'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    gl.useProgram(program);
    const uniforms = Object.fromEntries(UNIFORMS.map(u => [u, gl.getUniformLocation(program, u)]));
    const sizes = [canvas.width, 256, 64];
    const masks = sizes.map(s => { const c = document.createElement('canvas'); c.width = s; c.height = s; return c; });
    const textures = sizes.map((_, i) => {
      const t = gl.createTexture()!; gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.uniform1i(uniforms['uM' + i], i); return t;
    });
    return { gl, program, uniforms, textures, masks };
  } catch (error) { console.warn('Motor gráfico del tiempo profundo no disponible; se usa el pintor básico.', error); return null; }
}

/** Rasteriza las costas fechadas en Mercator y deriva dos versiones difuminadas (cercanía a la costa y continentalidad). */
function uploadMask(engine: Engine, coast: FeatureCollection) {
  const { gl, masks, textures } = engine, [full, mid, small] = masks, w = full.width, h = full.height, m = full.getContext('2d')!;
  m.fillStyle = '#000'; m.fillRect(0, 0, w, h); m.fillStyle = '#fff'; m.strokeStyle = '#fff'; m.lineWidth = w / 930; m.lineJoin = 'round';
  const point = (p: Position) => [(p[0] + 180) / 360 * w, (1 - Math.log(Math.tan(Math.PI / 4 + Math.max(-85.051, Math.min(85.051, p[1])) * Math.PI / 360)) / Math.PI) / 2 * h];
  for (const f of coast.features) {
    const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.type === 'MultiPolygon' ? f.geometry.coordinates : [];
    for (const poly of polys) { m.beginPath(); for (const ring of poly) { ring.forEach((p, i) => { const [x, y] = point(p); if (i === 0) m.moveTo(x, y); else m.lineTo(x, y); }); m.closePath(); } m.fill('evenodd'); m.stroke(); }
  }
  // Reducciones sucesivas (a la mitad cada vez) = difuminado barato y sin costuras al envolver en longitud.
  let source: HTMLCanvasElement = full;
  for (const target of [mid, small]) {
    let size = source.width;
    while (size > target.width) {
      const next = Math.max(target.width, size / 2), c = next === target.width ? target : document.createElement('canvas');
      if (c !== target) { c.width = next; c.height = next; }
      const ctx = c.getContext('2d')!; ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(source, 0, 0, next, next);
      source = c; size = next;
    }
  }
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  masks.forEach((c, i) => { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, textures[i]); gl.texImage2D(gl.TEXTURE_2D, 0, gl.R8, gl.RED, gl.UNSIGNED_BYTE, c); });
}

/** Prestaciones del dispositivo: con trazado por software (sin GPU) se reduce la textura y no se anima. */
let profile: { size: number; staticSize: number; animate: boolean } | undefined;
export function deepRenderProfile() {
  if (profile) return profile;
  profile = { size: 1024, staticSize: 1024, animate: false };
  try {
    const gl = document.createElement('canvas').getContext('webgl2');
    if (gl) {
      const info = gl.getExtension('WEBGL_debug_renderer_info');
      const name = String(info ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER));
      const software = /swiftshader|llvmpipe|software|basic render/i.test(name), max = gl.getParameter(gl.MAX_TEXTURE_SIZE) as number;
      const mobile = /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent);
      // Escenas animadas (magma, volcanes) a 2048 px para sostener la cadencia; escenas fijas a 4096 px en equipos de sobremesa.
      profile = software ? { size: 1024, staticSize: 1024, animate: false } : { size: Math.min(2048, max), staticSize: Math.min(mobile ? 2048 : 4096, max), animate: true };
      gl.getExtension('WEBGL_lose_context')?.loseContext();
    }
    // Ajuste manual opcional (p. ej. equipos modestos): localStorage «historicmap-deep-size» = 1024, 2048 o 4096.
    const forced = Number(localStorage.getItem('historicmap-deep-size'));
    if ([1024, 2048, 4096].includes(forced)) profile = { ...profile, staticSize: forced, size: Math.min(profile.size, forced) };
  } catch { /* sin WebGL2 o sin almacenamiento */ }
  return profile;
}
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
export const deepSurfaceAnimated = (scene: DeepScene) => deepRenderProfile().animate && (scene.mode === 'magma' || scene.mode === 'cooling' || scene.oldestMa > 3600);

interface Frame { scene: DeepScene; year: number; showIce: boolean; optics: 'standard' | 'ferruginous'; hasMask: boolean }
const frames = new WeakMap<HTMLCanvasElement, Frame>();

function render(canvas: HTMLCanvasElement, engine: Engine, frame: Frame, time: number) {
  const { gl, uniforms: u } = engine, { scene, year } = frame, age = (1950 - (year < 0 ? year + 1 : year)) / 1e6;
  const ice = frame.showIce ? deepIceAt(year) : null;
  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.uniform1f(u.uHasMask, frame.hasMask ? 1 : 0); gl.uniform1f(u.uLandFrac, scene.landFraction); gl.uniform1f(u.uTime, time); gl.uniform1f(u.uAge, age);
  gl.uniform1f(u.uProgress, clamp01((age - scene.youngestMa) / (scene.oldestMa - scene.youngestMa)));
  gl.uniform1f(u.uVeg, clamp01((470 - age) / 110));                          // de las primeras plantas terrestres a los bosques
  gl.uniform1f(u.uOxid, clamp01((2400 - age) / 300));                        // capas rojas tras la Gran Oxigenación
  gl.uniform1f(u.uCold, deepIceAt(year) ? 1 : .42);
  gl.uniform1f(u.uLush, scene.id === 'carboniferous' || scene.id === 'jurassic' || scene.id === 'cretaceous' ? 1 : 0);
  gl.uniform1f(u.uHaze, age >= 2500 && age <= 3400 ? .26 : 0);
  gl.uniform1f(u.uFerr, frame.optics === 'ferruginous' && age >= 2100 && age <= 2600 ? .74 : 0);
  gl.uniform1i(u.uMode, scene.mode === 'magma' ? 1 : scene.mode === 'cooling' ? 2 : 0);
  gl.uniform1i(u.uIce, ice ? ICE[ice] ?? 5 : 0);
  gl.uniform3fv(u.uOcean, rgb(scene.ocean)); gl.uniform3fv(u.uLand, rgb(scene.land));
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
}

/** Pinta la superficie de una escena del tiempo profundo. Misma interfaz que el pintor anterior. */
export function drawDeepSurface(canvas: HTMLCanvasElement, scene: DeepScene, year: number, coast?: FeatureCollection, showIce = true, optics: 'standard' | 'ferruginous' = 'standard', time = 0) {
  if (!engines.has(canvas)) engines.set(canvas, createEngine(canvas));
  const engine = engines.get(canvas);
  if (!engine) { try { drawCpu(canvas, scene, year, coast, showIce, optics); } catch { /* lienzo ya ligado a WebGL: sin pintor alternativo */ } return; }
  const p = deepRenderProfile(), size = deepSurfaceAnimated(scene) ? p.size : p.staticSize;
  if (canvas.width !== size) { canvas.width = canvas.height = size; engine.masks[0].width = engine.masks[0].height = size; }
  const hasMask = !!coast?.features.length;
  if (hasMask) uploadMask(engine, coast!);
  const frame = { scene, year, showIce, optics, hasMask }; frames.set(canvas, frame);
  render(canvas, engine, frame, time);
}
/** Repinta la última escena con otro instante de animación (magma, corteza, volcanes). */
export function animateDeepSurface(canvas: HTMLCanvasElement, time: number) {
  const engine = engines.get(canvas), frame = frames.get(canvas);
  if (!engine || !frame) return false;
  render(canvas, engine, frame, time); return true;
}
/** Color medio de la primera y la última fila de la textura (norte, sur): rellena los casquetes más allá de 85° de latitud. */
export function deepPoleColors(canvas: HTMLCanvasElement): [string, string] | undefined {
  const engine = engines.get(canvas); if (!engine) return;
  const { gl } = engine, w = canvas.width, row = new Uint8Array(w * 4);
  const mean = (y: number) => {
    gl.readPixels(0, y, w, 1, gl.RGBA, gl.UNSIGNED_BYTE, row);
    let r = 0, g = 0, b = 0; for (let i = 0; i < row.length; i += 4) { r += row[i]; g += row[i + 1]; b += row[i + 2]; }
    return '#' + [r, g, b].map(v => Math.round(v / w).toString(16).padStart(2, '0')).join('');
  };
  return [mean(canvas.height - 2), mean(1)];
}
