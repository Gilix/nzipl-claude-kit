# Frontend Gotchas

Issues specific to HTML deliverables, D3 charts, and browser rendering. Check here when debugging scrollytelling, play cards, or infrastructure maps.

For data pipeline and API issues, see `gotchas.md`.

## D3 / Browser

### Headless screenshots
Content more than ~8000px down the page renders black in headless browser screenshots. Workaround: clone the target slide to the top of the DOM before screenshotting.

### `const` redeclaration
If a draw function already declares a `const` variable in scope, do not redeclare it. JavaScript will throw a SyntaxError. Reuse the existing variable or use a different name.

### D3 transitions in headless
Transitions do not fire in headless preview environments. Use `.interrupt()` and set attributes directly for verification.
