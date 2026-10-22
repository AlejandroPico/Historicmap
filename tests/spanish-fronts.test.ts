import {readFileSync} from 'node:fs';
import {describe, expect, it} from 'vitest';
import type {Feature, FeatureCollection, MultiPolygon, Polygon, Position} from 'geojson';

const data=JSON.parse(readFileSync(new URL('../public/data/spanish-civil-war.geojson',import.meta.url),'utf8')) as FeatureCollection<Polygon|MultiPolygon>&{metadata:{registration:{sourceDate:string;minimumRegistrationUncertaintyMetres:number;maxResidualMetres:number}}};
const at=(year:number)=>data.features.filter(f=>f.properties!.start<=year&&f.properties!.end>=year);
const inRing=([x,y]:Position,ring:Position[])=>{
  let inside=false;
  for(let i=0,j=ring.length-1;i<ring.length;j=i++){
    const [ax,ay]=ring[i], [bx,by]=ring[j];
    if((ay>y)!==(by>y)&&x<(bx-ax)*(y-ay)/(by-ay)+ax)inside=!inside;
  }
  return inside;
};
const covers=(feature:Feature<Polygon|MultiPolygon>,point:Position)=>{
  const polygons=feature.geometry.type==='Polygon'?[feature.geometry.coordinates]:feature.geometry.coordinates;
  return polygons.some(rings=>inRing(point,rings[0])&&!rings.slice(1).some(ring=>inRing(point,ring)));
};
const controllers=(year:number,point:Position)=>at(year).filter(f=>covers(f,point)).map(f=>f.properties!.controller);
const ringArea=(ring:Position[])=>Math.abs(ring.reduce((sum,[x,y],i)=>{
  const [nx,ny]=ring[(i+1)%ring.length];return sum+x*ny-nx*y;
},0)/2);
const area=(f:Feature<Polygon|MultiPolygon>)=>{
  const polygons=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates;
  return polygons.reduce((sum,rings)=>sum+ringArea(rings[0])-rings.slice(1).reduce((holes,ring)=>holes+ringArea(ring),0),0);
};

describe('sourced Spanish Civil War control',()=>{
  it('has stable distinct dated factions and ends with a single victorious control',()=>{
    expect(data.features).toHaveLength(7);
    expect(new Set(data.features.map(f=>f.id)).size).toBe(7);
    expect(new Set(data.features.map(f=>f.properties!.uid)).size).toBe(7);
    expect(at(1935)).toHaveLength(0);expect(at(1940)).toHaveLength(0);
    for(const year of [1936,1937,1938]){
      expect(at(year)).toHaveLength(2);
      expect(new Set(at(year).map(f=>f.properties!.controller))).toEqual(new Set(['ESP-REPUBLIC','ESP-NATIONALIST']));
      expect(new Set(at(year).map(f=>f.properties!.controlColor)).size).toBe(2);
    }
    expect(at(1939)).toHaveLength(1);
    expect(at(1939)[0].properties!.controller).toBe('ESP-NATIONALIST');
  });
  it('shows the fall of the northern front and Málaga while Madrid and Barcelona remain republican',()=>{
    const north:Position[]=[[-2.935,43.263],[-5.6611,43.5357]]; // Bilbao, Gijón
    for(const point of [...north,[-4.4213,36.7213]]){
      expect(controllers(1936,point)).toEqual(['ESP-REPUBLIC']);
      expect(controllers(1937,point)).toEqual(['ESP-NATIONALIST']);
      expect(controllers(1938,point)).toEqual(['ESP-NATIONALIST']);
    }
    for(const point of [[-3.7038,40.4168],[2.1734,41.3851]]){
      for(const year of [1936,1937,1938])expect(controllers(year,point)).toEqual(['ESP-REPUBLIC']);
      expect(controllers(1939,point)).toEqual(['ESP-NATIONALIST']);
    }
    for(const year of [1936,1937,1938,1939]){
      expect(controllers(year,[-.8891,41.6488])).toEqual(['ESP-NATIONALIST']); // Zaragoza
      expect(controllers(year,[-5.9845,37.3891])).toEqual(['ESP-NATIONALIST']); // Sevilla
    }
  });
  it('partitions the same exterior and grows the winning control without claiming measured historical area',()=>{
    const extent=area(at(1939)[0]);let previous=0;
    for(const year of [1936,1937,1938,1939]){
      expect(at(year).reduce((sum,f)=>sum+area(f),0)).toBeCloseTo(extent,6);
      const national=area(at(year).find(f=>f.properties!.controller==='ESP-NATIONALIST')!);
      expect(national).toBeGreaterThan(previous);previous=national;
    }
  });
  it('retains the actual 1937 observation month, source attribution and registration limits',()=>{
    expect(data.metadata.registration.sourceDate).toBe('1937-10');
    expect(data.metadata.registration.minimumRegistrationUncertaintyMetres).toBeGreaterThanOrEqual(10000);
    expect(data.metadata.registration.maxResidualMetres).toBeLessThan(10000);
    for(const f of at(1937)){
      expect(f.properties!.note).toContain('octubre de 1937');
      expect(f.properties!.note).toContain('No es un frente diario');
      expect(f.properties!.license).toBe('CC-BY-SA-3.0');
      expect(f.properties!.attribution).toContain('Tyk');
      expect(f.properties!.source).toContain('GCE-Frente_en_oct_1937.svg');
    }
  });
});
