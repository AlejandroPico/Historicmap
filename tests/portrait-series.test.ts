import {it,expect} from 'vitest';
import {portraitAt,type PortraitCatalogue} from '../src/portrait-series';
const media=(file:string)=>({file,title:file,url:'https://example.org/photo',artist:'Author',license:'CC0',sha256:'fixture',bytes:1});
const catalogue:PortraitCatalogue={referenceDate:'2026-10-25',records:[{person:'Q1',start:2017,end:2021,media:media('first.jpg'),photoDate:'2017-01-20',dateLabel:'Fotografía de 2017',source:'https://example.org/first',note:''},{person:'Q1',start:2025,end:2026,media:media('second.jpg'),photoDate:'2025-01-20',dateLabel:'Fotografía de 2025',source:'https://example.org/second',note:''}]};
it('uses separate dated portraits in repeat mandates without assigning an office between them',()=>{
 expect(portraitAt('Q1',2020,'2017-01-20','2021-01-20',undefined,catalogue)?.file).toBe('first.jpg');
 expect(portraitAt('Q1',2025,'2025-01-20','2026-10-22',undefined,catalogue)?.file).toBe('second.jpg');
 expect(portraitAt('Q1',2023,'2017-01-20','2021-01-20',undefined,catalogue)).toBeUndefined();
 expect(portraitAt('Q2',2020,'2019-01-01','2022-01-01',media('fallback.jpg'),catalogue)?.file).toBe('fallback.jpg');
 expect(portraitAt('Q1',2020,'2017-01-20','2021-01-20',undefined,catalogue)?.photoDateLabel).toBe('Fotografía de 2017');
});
