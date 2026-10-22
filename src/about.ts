/** Product identity and release information, following the author's other projects. */
export function aboutContent(version:string,base:string){return `
  <header class="about-header">
    <div class="about-project-icon"><img src="${base}favicon.svg" width="64" height="64" alt=""></div>
    <div class="about-heading"><p>ATLAS DE LA TIERRA A TRAVÉS DEL TIEMPO</p><h2>historic<span>map</span></h2></div>
  </header>
  <div class="about-layout">
    <aside class="about-index"><h3>El proyecto</h3><dl>
      <div><dt>Versión</dt><dd>${version}</dd></div>
      <div><dt>Actualización</dt><dd>23 de octubre de 2026</dd></div>
      <div><dt>Exploración</dt><dd>Mapa 2D y globo 3D</dd></div>
      <div><dt>Cartografía</dt><dd>Desde 1789 por años · identidades fechadas</dd></div>
    </dl></aside>
    <div class="about-copy"><p class="about-lead">El tiempo tiene un lugar.</p><p>Un atlas para explorar la evolución de la Tierra y la historia de las sociedades humanas. Continentes, territorios y lugares, conectados por una misma línea temporal.</p>
      <div class="about-purpose"><h3>Explorar el atlas</h3><div><strong>Espacio</strong><span>Alterna entre mapa y globo. La rueda sobre el mapa ajusta su zoom.</span></div><div><strong>Tiempo</strong><span>Arrastra la regla para cambiar de fecha. La rueda sobre ella amplía o reduce la escala, manteniendo el momento seleccionado en el centro.</span></div><div><strong>Contexto</strong><span>Consulta capas, fuentes y metodología desde los botones de la esquina superior derecha.</span></div></div>
      <details class="release-history"><summary>Historial de versiones</summary><ol><li><strong>0.6.0 · 23 octubre 2026</strong><p>Ampliación mundial de autoridades, fotografías y banderas desde 1990; identidades de Estados predecesores, contextos y conflictos fechados. Catálogo de 27 organizaciones con altas y bajas históricas, Sáhara Occidental contextualizado, búsqueda compacta y tarde en tonos cálidos.</p></li><li><strong>0.5.0 · 22 octubre 2026</strong><p>Fichas por pestañas a la izquierda, mandatos de todo el año y ampliación mundial de retratos. Identidades y datos de territorios separados, temas mañana/tarde/noche/automático, fuentes compactas y capas de OTAN, UE, BRICS y Tres Mares en 2026.</p></li><li><strong>0.4.0 · 22 octubre 2026</strong><p>Cronología anual desde 1789, colores de régimen y control territorial opaco, Guerra Civil española, banderas históricas y autoridades fechadas con retratos y fuentes.</p></li><li><strong>0.3.0 · 22 octubre 2026</strong><p>Territorios y dependencias fechados de 1900–2019, síntesis territorial de la Segunda Guerra Mundial, ocupaciones y disputas, fichas ampliadas, capitales históricas, 323 ciudades actuales e indicadores económicos. Reproducción anual que espera la carga del mapa. Año máximo obtenido del dispositivo.</p></li><li><strong>0.2.0 · 22 octubre 2026</strong><p>Mapa a pantalla completa, herramientas compactas, capas desplegables y regla temporal con zoom independiente y controles integrados.</p></li><li><strong>0.1.0 · 21 octubre 2026</strong><p>Primera edición: mapa y globo, navegación temporal, 26 instantáneas y catálogo de fuentes.</p></li></ol></details>
      <p class="about-note">Un proyecto de Alejandro Pico. La cobertura histórica y el detalle cartográfico se amplían por etapas. Las reconstrucciones y sus incertidumbres se identifican en el atlas.</p>
    </div>
  </div>
  <nav class="about-links" aria-label="Enlaces del proyecto"><a href="https://alejandropico.github.io/Portfolio/" target="_blank" rel="noopener noreferrer"><span>Autor</span><strong>Alejandro Pico · Portfolio</strong><b>↗</b></a><a href="https://github.com/AlejandroPico/Historicmap" target="_blank" rel="noopener noreferrer"><span>Proyecto</span><strong>Historicmap · GitHub</strong><b>↗</b></a></nav>
  <div class="about-spectrum" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>`;}
