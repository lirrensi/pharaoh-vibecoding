# Security Review Router

> Split by trust boundary and attack surface.
>
> Report findings by issue name + location. Add CWE/CVE tags when relevant. Do not rely on checklist numbers.

## Modules

- `ph/security/core.md` - Input handling, secrets, logging, failure modes, and privacy controls that apply almost everywhere.
- `ph/security/identity.md` - Authentication, authorization, sessions, tenancy, and privilege boundaries.
- `ph/security/remote_surfaces.md` - Headers, APIs, browser/mobile surfaces, network edges, and abuse-prone exposed flows.
- `ph/security/execution_and_supply_chain.md` - Runtime, file/tool execution, CI/CD, agent/tool trust boundaries, and supply-chain risks.

## Common Loadouts

| Repo Shape | Load |
|------------|------|
| Web service / SaaS API | `core` + `identity` + `remote_surfaces` |
| Browser frontend | `core` + `remote_surfaces` |
| Local-first app / desktop / mobile | `core` + `remote_surfaces` + `execution_and_supply_chain` |
| CLI / scanner / extension / plugin | `core` + `execution_and_supply_chain` |
| AI or tool-using system | `core` + `execution_and_supply_chain` (+ `identity` if it acts on user/org data) |
| Broad platform / full-stack audit | Start with `core`, then add only the modules that match the repo's real surfaces |

## Loading Rule

- Start with this router.
- Load `ph/security/core.md` for nearly every security review.
- Add only the extra modules that match the codebase's actual trust boundaries.
- Load all four modules only for genuinely broad platform reviews.
