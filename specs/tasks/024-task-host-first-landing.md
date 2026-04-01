# Task 024: Host-First Landing Page

**Feature:** F-HOST (Host Personas & Landing Experience)
**Priority:** P0
**Dependencies:** 018 (Expand Hosts), 023 (Italian UI Translations)

## Description

Redesign the post-login experience so that the host selection page is the first screen users see. Hosts are grouped by target language (Italian, Danish, English) with clear section headings. Selecting a host sets both the target language and the persona, then navigates to the main categories page. Users who already have a saved host skip the landing page and go directly to categories.

## Technical Requirements

### New Host Selection Page
- A dedicated route/page (e.g., `/select-host`) displaying all available hosts
- Hosts grouped under language sections with headings: "Learn Italian", "Lær dansk", "Learn English" (in the user's reference language)
- Each host displayed as a card showing: portrait image, name, short personality description in the reference language
- Cards laid out in a responsive grid (1 column mobile, 2 tablet, 4 desktop within each language section)
- Tapping a host card:
  1. Saves the host selection to the user's profile via the existing profile API
  2. Navigates to the main categories page

### Routing Logic
- After login, if the user has no saved host (`hostId` is null or not set), redirect to `/select-host`
- After login, if the user has a saved host, proceed to the categories page as usual
- New user registration should NOT pre-set a default host — the user must choose

### Backend Profile Update
- Update the User model to allow `hostId` to be nullable (currently defaults to "marco")
- New registrations should set `hostId` to `null` instead of "marco"
- The profile API should accept any of the 12 valid host IDs

### Host Switcher (Top-Right Corner)
- Add a host indicator to the top-right area of the `Layout` component (visible on every page)
- The indicator shows the current host's portrait image (small, circular, ~32px)
- Clicking the indicator opens the full host selection page (navigate to `/select-host`)
- The host switcher is only visible when the user has a selected host

### Remove Existing Host Selector from Categories Page
- The existing `HostSelector` component on the categories page should be removed
- Host selection now only happens on the dedicated landing page and via the top-right switcher

## Acceptance Criteria

- [ ] After login with no host selected, the user is redirected to the host selection page
- [ ] The host selection page shows all 12 hosts grouped by language
- [ ] Each host card displays portrait image, name, and description in the user's reference language
- [ ] Selecting a host saves it to the profile and navigates to the categories page
- [ ] Returning users with a saved host go directly to categories
- [ ] A host avatar in the top-right corner is visible on every page
- [ ] Clicking the avatar navigates to the host selection page
- [ ] Switching to a host in a different language changes the word set displayed
- [ ] New registrations have no default host (must choose)
- [ ] The old HostSelector component is removed from the categories page

## Testing Requirements

- Unauthenticated users are redirected to login, not host selection
- Users without a host are redirected to host selection after login
- Users with a saved host skip host selection and see categories
- Selecting a host updates the user's profile
- Host switcher is present in the page layout
- All 12 hosts are rendered with correct language groupings
