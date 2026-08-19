import assert from "node:assert/strict";
import {
  CYCLE_LENGTH,
  getCycleDay,
  getShiftForDate,
  countWorkDaysInRange,
} from "../src/lib/rota";

assert.equal(getShiftForDate(new Date(2026, 0, 1)).kind, "off");
assert.equal(getShiftForDate(new Date(2026, 0, 2)).kind, "off");
assert.equal(getShiftForDate(new Date(2026, 0, 3)).kind, "day");
assert.equal(getShiftForDate(new Date(2026, 0, 4)).kind, "day");
assert.equal(getShiftForDate(new Date(2026, 0, 5)).kind, "night");
assert.equal(getShiftForDate(new Date(2026, 0, 6)).kind, "night");
assert.equal(getShiftForDate(new Date(2026, 0, 7)).kind, "off");
assert.equal(getShiftForDate(new Date(2026, 0, 10)).kind, "off");
assert.equal(getShiftForDate(new Date(2026, 0, 11)).kind, "day");
assert.equal(getShiftForDate(new Date(2026, 0, 12)).kind, "day");
assert.equal(getShiftForDate(new Date(2026, 0, 13)).kind, "night");
assert.equal(getShiftForDate(new Date(2026, 0, 14)).kind, "night");

assert.equal(CYCLE_LENGTH, 8);
assert.equal(getCycleDay(new Date(2026, 0, 3)), 0);

const jan = countWorkDaysInRange(new Date(2026, 0, 1), new Date(2026, 0, 31));
assert.equal(jan.days + jan.nights + jan.off, 31);
assert.ok(jan.hours > 0);

console.log("rota tests passed");
