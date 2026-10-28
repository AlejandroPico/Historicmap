import {isoYear,compareDates,dateYear} from './dates';
import catalogue from '../public/data/conflict-points.geojson?raw';
import type {FeatureCollection} from 'geojson';
const data=JSON.parse(catalogue) as FeatureCollection;
export function conflictPointsFor(year:number):FeatureCollection{
 const first=`${isoYear(year)}-01-01`,last=`${isoYear(year)}-12-31`;
 return {...data,features:data.features.filter(f=>compareDates(f.properties!.start,last)<=0&&compareDates(f.properties!.end,first)>=0)};
}
