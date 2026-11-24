import { describe, expect, it } from 'vitest';import { medicineCatalog, specialties } from '../data';
describe('SehatSetu data contracts',()=>{it('has routing specialties',()=>expect(specialties.length).toBeGreaterThanOrEqual(7));it('keeps medicine information non-prescriptive',()=>expect(medicineCatalog.every(x=>x.note.length>20)).toBe(true));});
