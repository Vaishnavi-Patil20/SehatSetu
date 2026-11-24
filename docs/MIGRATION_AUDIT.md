# Phase 1 audit — supplied SIH_Website-main

## Inventory reviewed
The supplied archive contains 949 paths, of which 18 are project source/config/assets after excluding `node_modules`, `.DS_Store`, generated dependencies and directories.

### Original UI
- `index.html` — Tailwind CDN landing page, navigation, feature cards, language selector.
- `login.html` + `login.css` — static login form; links point to routes such as `/register` and `/forgot-password` but no authentication implementation exists in the supplied source.
- `chatbot.html` — polished static chat shell with multilingual labels and quick actions; the inspected implementation does not contain a real ML inference integration.
- `basicQuestion.html` — adaptive questionnaire; answers are saved to browser `localStorage` and can be exported as JSON.
- `bookappointment.html` — specialty cards; selection currently triggers an alert rather than creating an appointment.
- `videoconsult.html` — video consultation mock interface; video stream is explicitly a placeholder and doctor data are placeholders; chat is local DOM-only.
- `medicines.html` — substantial client-side medicine catalogue, search/filter/pagination/cart logic. Cart is persisted in `localStorage`; checkout explicitly reports that it is a demo.
- `checker.html` — retained as legacy reference and reviewed as part of the original flow.

### Original logic/assets
- `script.js` — hardcoded translations for a limited set of homepage strings.
- `translation.js` — separate translation implementation that calls `http://localhost:5000/api/translate`, creating overlapping translation approaches.
- `style.css` — mixed global styles and Tailwind-era component styles.
- `Logo(EP).png`, `GOP.svg`, `healthcare.jpg` — original assets preserved under `legacy/`.

### Original backend
`legacy/backend/server.js` contains a single Express endpoint `/api/translate` that proxies LibreTranslate. It listens on port 5000. There is no original authentication, query persistence, ML model service, appointment API, role system or database layer in the inspected backend.

## Migration decisions
1. Preserve the complete original source under `legacy/` rather than deleting it.
2. Replace the static frontend with a modular React + TypeScript + Vite application.
3. Replace the external chatbot as the primary decision engine with a first-party FastAPI classifier.
4. Keep medicine information as informational UX; do not turn it into prescription generation.
5. Treat video consultation as an integration boundary: real provider credentials/infrastructure are required before claiming live calls.
6. Use Supabase for authentication, profiles, query history, appointments and RLS.
7. Keep the original multilingual ambition, but ship reliable English first in the new core workflow; language expansion should use a documented/tested translation layer.

## Known limitations of the supplied project
- No persistent authentication.
- No database/RLS.
- No real ML inference service.
- Appointment selection is UI-only.
- Video call is a placeholder.
- Medicine checkout is a demo.
- Translation logic is duplicated and partly dependent on localhost + an external translation endpoint.
- Several pages use remote image/CDN references rather than local, controlled assets.

## Verification principle
A feature is not labelled production-ready merely because a button exists. The new SehatSetu README and research documentation explicitly distinguish implemented logic, configured integrations and demo-only boundaries.
