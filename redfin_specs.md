# Redfin.com — Functional Requirements & Acceptance Criteria

**Version:** 1.1
**Product:** Redfin.com
**Scope:** Consumer website and associated real-estate services

---

# Part A — Functional Requirements and Acceptance Criteria

## 1. Purpose and Acceptance Criteria Approach

The purpose of this document is to specify the functionality of Redfin's real-estate platform and define the conditions under which each capability can be considered acceptable.

Acceptance criteria describe observable system behavior. They can be used to develop manual test cases, automated tests, and end-to-end validation scenarios.

### Acceptance Criteria Conventions

* **Given** — the precondition or initial system state.
* **When** — the user action or system event.
* **Then** — the expected result.
* **Where supported / applicable** — functionality that depends on a particular listing, market, account type, or service availability.
* **Pass condition** — all applicable criteria for a requirement are satisfied.

The criteria below specify intended behavior. They are not a claim that every feature has been independently tested or that every feature is available in every market or on every device.

---

# 2. Product Overview

## FR-001 — Real-estate Platform

The platform shall allow users to discover, evaluate, save, share, and act on real-estate listings, and access associated buying, selling, rental, and market-information services.

### Acceptance Criteria

* **AC-001.1:** Given a visitor opens Redfin, when the homepage loads, then the visitor can access the available property-search and real-estate service entry points.
* **AC-001.2:** Given a user selects a supported service, when the service page opens, then the system displays the appropriate functionality for that service.
* **AC-001.3:** Given a user navigates between supported sections, when the destination loads, then the system preserves the user's session and applicable account state.
* **AC-001.4:** Given a feature is unavailable for a particular listing or location, when the user accesses that feature, then the system communicates its unavailability without presenting fabricated information.

---

# 3. User Types

## FR-001 — Anonymous Visitor

### Acceptance Criteria

* **AC-001.1:** Given a user is not signed in, when they open a publicly accessible listing, then they can view the listing information available to anonymous visitors.
* **AC-001.2:** Given an anonymous user performs a property search, when they submit valid search criteria, then matching results are displayed without requiring registration.
* **AC-001.3:** Given an anonymous user attempts an account-restricted action, when they select that action, then the system prompts them to sign in or register, as applicable.

## FR-002 — Registered User

### Acceptance Criteria

* **AC-002.1:** Given a registered user is authenticated, when they save a property, then it is associated with their account.
* **AC-002.2:** Given a user updates account preferences, when they save the changes, then the updated preferences are retained.
* **AC-002.3:** Given a user signs out and subsequently signs in again, then their saved properties, saved searches, and other persisted account data remain available.

## FR-003 — Buyer

### Acceptance Criteria

* **AC-003.1:** Given a buyer searches for homes, when they apply supported filters, then the results reflect those filters.
* **AC-003.2:** Given a buyer opens an eligible listing, when they request a tour or agent contact, then the system presents the applicable next steps.
* **AC-003.3:** Given a buyer saves a property, when they revisit their account, then the property is accessible from their saved items.

## FR-004 — Renter

### Acceptance Criteria

* **AC-004.1:** Given a renter enters a location and rental criteria, when they submit the search, then matching rental listings are displayed.
* **AC-004.2:** Given a renter opens a rental listing, when they select the contact option, then the system presents the available property-manager contact process.
* **AC-004.3:** Given a renter saves a supported rental search, when matching rental listings become available, then notifications are delivered according to the configured preferences.

## FR-005 — Seller

### Acceptance Criteria

* **AC-005.1:** Given a homeowner enters a supported property address, when they request a home estimate, then the system displays an estimate if available.
* **AC-005.2:** Given a seller requests a consultation, when the request is submitted successfully, then the system confirms submission.
* **AC-005.3:** Given a seller begins a listing process, when required information is provided, then the system advances the seller to the next applicable step.

## FR-006 — Agent

### Acceptance Criteria

* **AC-006.1:** Given an authorized agent accesses an agent-specific service, when authentication and authorization succeed, then the agent can access permitted functions.
* **AC-006.2:** Given an agent receives a customer inquiry, when it is successfully routed, then the inquiry is accessible through the supported agent workflow.
* **AC-006.3:** Given an agent attempts an action outside their permissions, when the action is submitted, then the system denies the action.

---

# 4. Home Page

## FR-010 — Homepage

### Acceptance Criteria

* **AC-010.1:** Given a visitor opens the homepage, then the page displays the primary navigation, location-search entry point, and available real-estate service links.
* **AC-010.2:** Given featured listings or market content are available, then the homepage displays the corresponding content.
* **AC-010.3:** Given a user selects a homepage navigation option, then the system opens the correct destination.
* **AC-010.4:** Given the user is signed in, then applicable account-specific navigation is available.

## FR-011 — Search Entry

### Acceptance Criteria

* **AC-011.1:** Given the user enters a valid supported location, when they submit it, then the system resolves the location and opens the relevant results.
* **AC-011.2:** Given the user enters an exact property address, when a matching property is found, then the system provides access to that property.
* **AC-011.3:** Given the search term is ambiguous, when multiple matches are available, then the system provides options to select the intended location.
* **AC-011.4:** Given no match is found, then the system displays an appropriate no-match message or recovery options.

---

# 5. Property Search

## FR-020 — Search by Location

### Acceptance Criteria

* **AC-020.1:** Given a supported city, ZIP code, neighborhood, address, or MLS identifier is entered, when the search is submitted, then the system returns the corresponding results or property.
* **AC-020.2:** Given a location has multiple possible matches, then the user can identify the intended location.
* **AC-020.3:** Given the selected location changes, then the results update to the new geographic scope.

## FR-021 — Multiple-Area Search

### Acceptance Criteria

* **AC-021.1:** Given the user enters multiple supported locations, when the search is submitted, then results from the selected locations are included.
* **AC-021.2:** Given a property falls within overlapping search areas, then it is not unnecessarily duplicated in the combined results.
* **AC-021.3:** Given one selected location is invalid, then the system identifies the invalid location without silently substituting a different one.

## FR-022 — Map Search

### Acceptance Criteria

* **AC-022.1:** Given search results are available, then the system displays property markers in the corresponding geographic area.
* **AC-022.2:** Given the user selects a marker, then the system displays the associated property summary.
* **AC-022.3:** Given the user pans or zooms the map, then the map responds to the interaction.
* **AC-022.4:** Given map-based searching is enabled, then the displayed properties correspond to the active search scope and filters.

## FR-023 — Draw Search Area

### Acceptance Criteria

* **AC-023.1:** Given the map supports custom-area search, when the user draws a valid boundary, then the selected boundary is visibly represented.
* **AC-023.2:** Given the user applies the boundary, then results are restricted to the selected area, subject to the platform's geographic-search behavior.
* **AC-023.3:** Given the user edits or clears the boundary, then the search scope updates accordingly.
* **AC-023.4:** Given the boundary is invalid or cannot be processed, then the system informs the user and does not apply an unintended area.

## FR-024 — Search Results

### Acceptance Criteria

* **AC-024.1:** Given matching listings exist, then each result displays the available primary listing information, such as photo, price, address, beds, baths, and property area.
* **AC-024.2:** Given a user selects a result, then the corresponding property-detail page opens.
* **AC-024.3:** Given a listing has no photograph or a particular data field, then the system displays an appropriate fallback or omits the unavailable field.
* **AC-024.4:** Given no properties match, then the system displays a clear empty state.

---

# 6. Search Filters

## FR-030 — Price Filter

### Acceptance Criteria

* **AC-030.1:** Given the user specifies a minimum and/or maximum price, when the filter is applied, then displayed listings satisfy the supported price bounds.
* **AC-030.2:** Given the minimum price exceeds the maximum price, then the system identifies the invalid range.
* **AC-030.3:** Given the user clears the price filter, then the results are no longer restricted by that filter.

## FR-031 — Bedroom Filter

### Acceptance Criteria

* **AC-031.1:** Given a minimum bedroom count is selected, then results satisfy that minimum according to Redfin's filter semantics.
* **AC-031.2:** Given the bedroom filter is changed, then the result set updates.
* **AC-031.3:** Given the filter is cleared, then the bedroom restriction is removed.

## FR-032 — Bathroom Filter

### Acceptance Criteria

* **AC-032.1:** Given a bathroom threshold is selected, then results meet the selected threshold according to the available filter options.
* **AC-032.2:** Given the user changes the threshold, then results update.
* **AC-032.3:** Given the filter is cleared, then the bathroom restriction is removed.

## FR-033 — Property-Type Filter

### Acceptance Criteria

* **AC-033.1:** Given one or more property types are selected, then results include only listings matching the selected types.
* **AC-033.2:** Given the user selects multiple types, then the system applies the supported combination logic.
* **AC-033.3:** Given a type is deselected, then the results update accordingly.

## FR-034 — Square-Footage Filter

### Acceptance Criteria

* **AC-034.1:** Given minimum and maximum area values are selected, then matching results satisfy the specified range.
* **AC-034.2:** Given the range is invalid, then the system identifies the issue.
* **AC-034.3:** Given a listing has no reported area, then it is handled consistently with the platform's filter rules and is not assigned an invented area.

## FR-035 — Additional Property Filters

### Acceptance Criteria

* **AC-035.1:** Given a supported filter such as lot size, year built, parking, or amenities is selected, then the system applies the filter to the results.
* **AC-035.2:** Given multiple filters are active, then the result set satisfies the combined criteria.
* **AC-035.3:** Given the user resets filters, then all applicable filters return to their default state.
* **AC-035.4:** Given a filter is not supported for the selected property category, then it is unavailable or clearly identified as inapplicable.

## FR-036 — Listing Status Filters

### Acceptance Criteria

* **AC-036.1:** Given the user selects a supported listing status, then results reflect that status selection.
* **AC-036.2:** Given a listing's status changes, then the displayed status updates when refreshed data becomes available.
* **AC-036.3:** Given a status is not offered for the current search, then the system does not imply that the filter was applied.

## FR-037 — Advanced Filtering

### Acceptance Criteria

* **AC-037.1:** Given the user opens advanced filters, then the available additional criteria are displayed.
* **AC-037.2:** Given advanced criteria are selected and applied, then the results reflect them.
* **AC-037.3:** Given the user closes the filter panel without applying changes, then the system follows its defined behavior for retaining or discarding the draft selections.
* **AC-037.4:** Given active filters are present, then the interface provides a way to identify and remove them.

---

# 7. Conversational Search

## FR-040 — Natural-Language Search

### Acceptance Criteria

* **AC-040.1:** Given a user enters a supported natural-language property request, when it is submitted, then the system interprets the request and presents relevant results.
* **AC-040.2:** Given the request contains recognizable criteria, then those criteria are reflected in the resulting search where supported.
* **AC-040.3:** Given the request cannot be interpreted, then the system asks for clarification or offers a usable alternative.
* **AC-040.4:** Given the request includes a criterion that cannot be searched directly, then the system does not falsely claim that the criterion has been verified.

## FR-041 — Conversational Refinement

### Acceptance Criteria

* **AC-041.1:** Given an initial conversational search has returned results, when the user requests a refinement, then the system updates the search accordingly.
* **AC-041.2:** Given the user adds a new criterion, then existing criteria are retained unless the user changes or removes them.
* **AC-041.3:** Given the refinement produces no matches, then the system communicates that outcome.

## FR-042 — Contextual Search

### Acceptance Criteria

* **AC-042.1:** Given a multi-turn search session, then follow-up requests are interpreted in the context of the active search.
* **AC-042.2:** Given the user explicitly changes a prior preference, then the updated preference takes precedence.
* **AC-042.3:** Given the context is insufficient to determine the user's intent, then the system requests clarification rather than silently guessing.

## FR-043 — Property-Specific Refinement

### Acceptance Criteria

* **AC-043.1:** Given a user refers to a displayed property or result, then the system identifies the intended context when unambiguous.
* **AC-043.2:** Given the user requests a similar property or a change to the search, then the system applies the supported refinement.
* **AC-043.3:** Given the referenced property cannot be identified, then the system asks the user to clarify.

---

# 8. Search Results

## FR-050 — Result Display

### Acceptance Criteria

* **AC-050.1:** Given a search returns listings, then the system presents them in the supported list/card and map interfaces.
* **AC-050.2:** Given a user switches views, then the same active search criteria are retained.
* **AC-050.3:** Given a result is selected, then the correct listing is opened.

## FR-051 — Result Sorting

### Acceptance Criteria

* **AC-051.1:** Given the user selects an available sort option, then the result ordering follows that option.
* **AC-051.2:** Given the sort order changes, then active filters remain applied.
* **AC-051.3:** Given a sort option is unavailable, then it is not presented as selectable.

## FR-052 — Result Navigation

### Acceptance Criteria

* **AC-052.1:** Given a user selects a listing, then the correct detail page opens.
* **AC-052.2:** Given the user returns to results, then the system preserves the search context where supported.
* **AC-052.3:** Given a listing URL is invalid or unavailable, then an appropriate error or unavailable-property state is displayed.

## FR-053 — Result Count

### Acceptance Criteria

* **AC-053.1:** Given a result count is available, then the interface displays a count corresponding to the active search.
* **AC-053.2:** Given filters change, then the displayed count updates.
* **AC-053.3:** Given the exact count cannot be determined, then the system does not display a fabricated count.

## FR-054 — Result Updates

### Acceptance Criteria

* **AC-054.1:** Given listing data changes at the source, then Redfin reflects the change when updated data becomes available.
* **AC-054.2:** Given a listing is no longer available, then the system reflects the applicable status or availability state.
* **AC-054.3:** Given the user refreshes results, then the system retrieves or displays the latest data available to the service.

---

# 9. Property Detail Page

## FR-060 — Property Overview

### Acceptance Criteria

* **AC-060.1:** Given a valid listing is opened, then the page displays its available address, price, property type, beds, baths, and area.
* **AC-060.2:** Given a field is unavailable, then the system omits it or clearly identifies it as unavailable.
* **AC-060.3:** Given the listing status or price changes, then the detail page reflects the updated information when available.

## FR-061 — Property Photographs

### Acceptance Criteria

* **AC-061.1:** Given photographs are available, then the user can view them on the detail page.
* **AC-061.2:** Given multiple photographs are available, then the user can navigate between them.
* **AC-061.3:** Given a photograph fails to load, then the system displays a fallback rather than a broken or misleading image.
* **AC-061.4:** Given no photographs are available, then the page remains usable.

## FR-062 — Property Description

### Acceptance Criteria

* **AC-062.1:** Given a listing description is available, then it is displayed with the corresponding property.
* **AC-062.2:** Given no description is available, then the page does not display an invented description.
* **AC-062.3:** Given the description contains formatting, then it is rendered legibly and safely.

## FR-063 — Property Features

### Acceptance Criteria

* **AC-063.1:** Given property features are provided, then the detail page displays the available features.
* **AC-063.2:** Given features are grouped into categories, then the user can identify the relevant category.
* **AC-063.3:** Given a feature is not confirmed, then it is not presented as a verified property attribute.

## FR-064 — Financial Information

### Acceptance Criteria

* **AC-064.1:** Given tax, HOA, or payment information is available, then it is displayed with an appropriate label.
* **AC-064.2:** Given a payment amount is an estimate, then the interface identifies it as an estimate.
* **AC-064.3:** Given financial information is missing, then the system does not infer an exact value without an identified calculation or source.

## FR-065 — Property History

### Acceptance Criteria

* **AC-065.1:** Given property history is available, then the system displays the relevant dated events.
* **AC-065.2:** Given multiple historical events exist, then they are distinguishable by date and event type.
* **AC-065.3:** Given history is unavailable or incomplete, then the system communicates that limitation.

## FR-066 — Price Changes

### Acceptance Criteria

* **AC-066.1:** Given a listing has recorded price changes, then the system displays available prior and current prices with applicable dates.
* **AC-066.2:** Given a price change is displayed, then it is associated with the correct listing.
* **AC-066.3:** Given there is no recorded price change, then the system does not imply that a reduction occurred.

## FR-067 — Listing Information

### Acceptance Criteria

* **AC-067.1:** Given listing-agent, brokerage, MLS, or listing-date information is available, then it is displayed accurately.
* **AC-067.2:** Given a listing status is displayed, then it corresponds to the available listing data.
* **AC-067.3:** Given an agent or brokerage detail is selectable, then it opens the corresponding supported destination.

---

# 10. Multimedia Property Experience

## FR-070 — Video

### Acceptance Criteria

* **AC-070.1:** Given a property video is available, then the user can initiate playback.
* **AC-070.2:** Given playback is unavailable, then the system communicates the failure and preserves access to other listing content.
* **AC-070.3:** Given the video is loading, then the interface provides an appropriate loading state.

## FR-071 — 3D Tours

### Acceptance Criteria

* **AC-071.1:** Given a 3D tour is available, then the user can launch the tour.
* **AC-071.2:** Given the tour loads successfully, then the user can interact with the supported 3D experience.
* **AC-071.3:** Given no 3D tour exists, then the page does not display a working-tour control.

## FR-072 — Virtual Tours

### Acceptance Criteria

* **AC-072.1:** Given a virtual tour is available, then the user can access it.
* **AC-072.2:** Given the tour requires an external viewer, then the user is directed to the appropriate destination.
* **AC-072.3:** Given the tour is unavailable, then the system provides a clear fallback.

---

# 11. Property Valuation and Estimates

## FR-080 — Property Estimate

### Acceptance Criteria

* **AC-080.1:** Given a supported property has an available Redfin Estimate, then the system displays the estimate.
* **AC-080.2:** Given no estimate is available, then the system communicates that no estimate is available.
* **AC-080.3:** Given an estimate is displayed, then it is identified as an estimate rather than a guaranteed sale price.

## FR-081 — Estimate Information

### Acceptance Criteria

* **AC-081.1:** Given explanatory estimate information is available, then the user can access it.
* **AC-081.2:** Given the estimate has a displayed date or update context, then that context is shown.
* **AC-081.3:** Given an estimate is unavailable or limited, then the system does not imply greater precision than the source supports.

## FR-082 — Estimate History

### Acceptance Criteria

* **AC-082.1:** Given historical estimates are available, then the user can view the supported history.
* **AC-082.2:** Given historical values are shown, then their dates are distinguishable.
* **AC-082.3:** Given history is unavailable, then no historical values are fabricated.

## FR-083 — Comparable Properties

### Acceptance Criteria

* **AC-083.1:** Given comparable properties are available, then the system displays the applicable comparable-property information.
* **AC-083.2:** Given a comparable property is selected, then its detail page opens where accessible.
* **AC-083.3:** Given comparables are estimates or algorithmically selected, then the system does not represent them as a formal appraisal.

## FR-084 — Property Value Updates

### Acceptance Criteria

* **AC-084.1:** Given an estimate is recalculated, then the current estimate reflects the updated value when available.
* **AC-084.2:** Given the estimate changes, then any supported history or change indicator is updated consistently.
* **AC-084.3:** Given the estimate has not changed, then the system does not report a change.

---

# 12. Neighborhood Information

## FR-090 — Neighborhood Information

### Acceptance Criteria

* **AC-090.1:** Given neighborhood information is available for a property, then the page displays the associated information.
* **AC-090.2:** Given the user opens a neighborhood destination, then the system displays the corresponding geographic area.
* **AC-090.3:** Given information is unavailable, then the system identifies the limitation.

## FR-091 — Market Statistics

### Acceptance Criteria

* **AC-091.1:** Given market statistics are available, then the system displays them with the applicable geographic context.
* **AC-091.2:** Given statistics represent a specific period, then the period is identifiable.
* **AC-091.3:** Given statistics are unavailable, then the system does not substitute unrelated market data.

## FR-092 — Schools

### Acceptance Criteria

* **AC-092.1:** Given school information is available, then the system displays the relevant school details.
* **AC-092.2:** Given school information is associated with a property or area, then the relationship is clearly represented.
* **AC-092.3:** Given school data is missing or potentially outdated, then the system does not imply that it has been independently verified as current.

## FR-093 — Neighborhood Search

### Acceptance Criteria

* **AC-093.1:** Given a user selects or enters a supported neighborhood, then the system displays properties in the corresponding search area.
* **AC-093.2:** Given the neighborhood has an ambiguous name, then the user can select the intended location.
* **AC-093.3:** Given the neighborhood has no matching listings, then the system displays an empty state.

---

# 13. Favorites

## FR-100 — Favorite Property

### Acceptance Criteria

* **AC-100.1:** Given an authenticated user selects Favorite, then the property is added to their saved favorites.
* **AC-100.2:** Given the save succeeds, then the interface reflects the saved state.
* **AC-100.3:** Given the save fails, then the interface communicates the failure and does not falsely confirm success.

## FR-101 — Remove Favorite

### Acceptance Criteria

* **AC-101.1:** Given a property is favorited, when the user removes it, then it is removed from the applicable favorite collection.
* **AC-101.2:** Given removal succeeds, then the interface reflects the updated state.
* **AC-101.3:** Given removal fails, then the system preserves the actual saved state and reports the failure.

## FR-102 — Favorite Lists

### Acceptance Criteria

* **AC-102.1:** Given a user creates a favorite list, then the list is available in their account.
* **AC-102.2:** Given a user adds a property to a list, then it appears in that list.
* **AC-102.3:** Given a user renames or deletes a list, then the change is reflected in the account.
* **AC-102.4:** Given a property is removed from one list, then it remains in other lists unless separately removed.

## FR-103 — Favorite Updates

### Acceptance Criteria

* **AC-103.1:** Given a favorited property has a supported price or status update, then the system reflects that update.
* **AC-103.2:** Given notifications are enabled for the relevant event, then the system sends the applicable notification.
* **AC-103.3:** Given notifications are disabled, then the system does not send that category of notification.

---

# 14. Hidden Properties

## FR-110 — Hide Property

### Acceptance Criteria

* **AC-110.1:** Given the user selects Hide on an eligible property, then the system records the hidden state.
* **AC-110.2:** Given the property is hidden, then it is excluded from applicable result or recommendation surfaces according to the feature's behavior.
* **AC-110.3:** Given the hide action fails, then the system does not falsely indicate that the property was hidden.

## FR-111 — Manage Hidden Properties

### Acceptance Criteria

* **AC-111.1:** Given hidden-property management is available, then the user can view hidden properties.
* **AC-111.2:** Given the user unhides a property, then the hidden state is removed.
* **AC-111.3:** Given a property is unhidden, then it may appear again in relevant results or recommendations.

---

# 15. Saved Searches

## FR-120 — Save Search

### Acceptance Criteria

* **AC-120.1:** Given a user saves a search, then the location and applicable filters are retained.
* **AC-120.2:** Given the user reopens the saved search, then the system restores the saved criteria.
* **AC-120.3:** Given the user is not authenticated, then the system prompts for authentication if saving requires an account.

## FR-121 — Name Saved Search

### Acceptance Criteria

* **AC-121.1:** Given a user names a saved search, then the name is associated with that search.
* **AC-121.2:** Given the user changes the name, then the updated name is displayed.
* **AC-121.3:** Given an invalid or unsupported name is entered, then the system communicates the validation issue.

## FR-122 — Edit Saved Search

### Acceptance Criteria

* **AC-122.1:** Given a saved search is edited, then the user can change its supported location and filters.
* **AC-122.2:** Given changes are saved, then reopening the search reflects the new criteria.
* **AC-122.3:** Given the user cancels editing, then unsaved changes are not incorrectly represented as saved.

## FR-123 — Delete Saved Search

### Acceptance Criteria

* **AC-123.1:** Given a user deletes a saved search, then it is removed from the saved-search collection.
* **AC-123.2:** Given deletion succeeds, then the deleted search is no longer available as an active saved search.
* **AC-123.3:** Given deletion fails, then the system communicates the failure.

## FR-124 — Saved-Search Notifications

### Acceptance Criteria

* **AC-124.1:** Given a saved search has notifications enabled, then eligible matching listings can trigger notifications.
* **AC-124.2:** Given the user changes notification frequency, then subsequent notifications follow the updated preference.
* **AC-124.3:** Given notifications are disabled, then the system does not send saved-search alerts.
* **AC-124.4:** Given a listing does not meet the saved criteria, then it is not represented as a match for that search.

---

# 16. Notifications and Alerts

## FR-130 — Listing Alerts

### Acceptance Criteria

* **AC-130.1:** Given a matching new listing is available and the user has enabled the relevant alert, then the system sends the applicable notification.
* **AC-130.2:** Given a notification is selected, then it opens the associated listing or relevant destination.
* **AC-130.3:** Given no eligible new listing exists, then no new-listing alert is generated for that event.

## FR-131 — Price Alerts

### Acceptance Criteria

* **AC-131.1:** Given a tracked property has a recorded price change, then the system can generate a price-change alert when enabled.
* **AC-131.2:** Given a price alert is opened, then the user can access the corresponding property.
* **AC-131.3:** Given no price change has occurred, then the system does not generate a price-change event.

## FR-132 — Status Alerts

### Acceptance Criteria

* **AC-132.1:** Given a tracked listing's status changes, then the system can generate an alert when enabled.
* **AC-132.2:** Given the alert is opened, then the property and its current available status are displayed.
* **AC-132.3:** Given the status has not changed, then a duplicate status-change event is not falsely reported.

## FR-133 — Open-House Alerts

### Acceptance Criteria

* **AC-133.1:** Given an eligible property has an open house and the relevant alert is enabled, then the user receives the applicable notification.
* **AC-133.2:** Given an open-house time changes or is canceled, then the system reflects the updated information when available.
* **AC-133.3:** Given the event is no longer scheduled, then it is not presented as an upcoming confirmed open house.

## FR-134 — Saved-Search Alerts

### Acceptance Criteria

* **AC-134.1:** Given new properties match an enabled saved search, then the system generates notifications according to the user's settings.
* **AC-134.2:** Given multiple matching listings are included in a notification, then each displayed listing corresponds to the saved search.
* **AC-134.3:** Given a saved search is deleted or its alerts are disabled, then future alerts for that search stop.

## FR-135 — Recommended Properties

### Acceptance Criteria

* **AC-135.1:** Given recommendation functionality is available, then the system displays properties selected according to supported recommendation logic.
* **AC-135.2:** Given the user opens a recommendation, then the correct property detail page is displayed.
* **AC-135.3:** Given the user hides or dismisses a recommendation, then the system reflects that action according to the supported behavior.
* **AC-135.4:** Given no recommendations are available, then the system provides an appropriate empty state.

## FR-136 — Notification Preferences

### Acceptance Criteria

* **AC-136.1:** Given the user changes a notification setting, then the system saves the preference.
* **AC-136.2:** Given the user revisits notification settings, then the saved preference is displayed.
* **AC-136.3:** Given a category is disabled, then notifications in that category are suppressed, subject to any explicitly disclosed exceptions.
* **AC-136.4:** Given the user changes frequency, then future notifications follow the selected supported frequency.

---

# 17. Sharing and Collaboration

## FR-140 — Share Property

### Acceptance Criteria

* **AC-140.1:** Given a user selects Share, then the system provides the supported sharing options.
* **AC-140.2:** Given a share link is generated, then it resolves to the intended property or supported destination.
* **AC-140.3:** Given sharing fails, then the system communicates the failure.

## FR-141 — Shared Favorites

### Acceptance Criteria

* **AC-141.1:** Given a user shares or invites another user to a supported favorite collection, then the invitation or sharing action is processed.
* **AC-141.2:** Given the recipient has the required access, then they can view the shared content.
* **AC-141.3:** Given access is revoked, then the recipient can no longer access the shared content through that permission.

## FR-142 — Collaborative Comments

### Acceptance Criteria

* **AC-142.1:** Given commenting is supported for a shared property, then an authorized user can submit a comment.
* **AC-142.2:** Given a comment is successfully submitted, then it appears in the appropriate shared context.
* **AC-142.3:** Given a user lacks permission, then they cannot submit or modify comments in that context.
* **AC-142.4:** Given comment submission fails, then the system does not falsely display it as successfully posted.

## FR-143 — Co-Buyer Collaboration

### Acceptance Criteria

* **AC-143.1:** Given users have access to a shared collection, then they can view the properties permitted by that collection.
* **AC-143.2:** Given one authorized user adds a property or comment, then other authorized users can see the update when synchronized.
* **AC-143.3:** Given users have different permissions, then each user's available actions reflect those permissions.

---

# 18. Property Tours

## FR-150 — Request Tour

### Acceptance Criteria

* **AC-150.1:** Given a property supports tours, then the user can initiate a tour request.
* **AC-150.2:** Given a property does not support the selected tour option, then the option is unavailable or clearly explained.
* **AC-150.3:** Given the user submits a valid request, then the system processes it and provides an appropriate response.

## FR-151 — Select Date

### Acceptance Criteria

* **AC-151.1:** Given tour scheduling is available, then the user can select an eligible date.
* **AC-151.2:** Given a date has no available tour options, then the system does not present it as available.
* **AC-151.3:** Given the selected date becomes unavailable before submission, then the user is prompted to select another date.

## FR-152 — Select Time

### Acceptance Criteria

* **AC-152.1:** Given a date is selected, then the system displays available time options when available.
* **AC-152.2:** Given the user selects an available time, then that time is associated with the request.
* **AC-152.3:** Given the time slot is no longer available at submission, then the system reports the conflict and offers alternatives where possible.

## FR-153 — Tour Confirmation

### Acceptance Criteria

* **AC-153.1:** Given a tour is successfully confirmed, then the system displays the confirmed date, time, and property.
* **AC-153.2:** Given the tour is only a request pending confirmation, then the system clearly distinguishes it from a confirmed appointment.
* **AC-153.3:** Given confirmation fails, then the system does not display the tour as confirmed.

## FR-154 — Tour Management

### Acceptance Criteria

* **AC-154.1:** Given the user has scheduled tours, then they can view applicable tour details.
* **AC-154.2:** Given cancellation or rescheduling is supported, then the user can initiate the action.
* **AC-154.3:** Given a tour is canceled or rescheduled successfully, then the updated state is displayed.
* **AC-154.4:** Given the user has no tours, then the system displays an appropriate empty state.

## FR-155 — Agent-Assisted Tour

### Acceptance Criteria

* **AC-155.1:** Given an agent-assisted tour is available, then the user can request that option.
* **AC-155.2:** Given an agent is assigned or confirmed, then the system displays the available appointment details.
* **AC-155.3:** Given no agent or time is available, then the system communicates the limitation and available next steps.

---

# 19. Tour Insights

## FR-160 — Tour Insights

### Acceptance Criteria

* **AC-160.1:** Given tour insights are available for a property, then the user can access them.
* **AC-160.2:** Given an insight is displayed, then it is associated with the relevant property.
* **AC-160.3:** Given no insights exist, then the system does not fabricate agent observations.

## FR-161 — Insight Categories

### Acceptance Criteria

* **AC-161.1:** Given insights are categorized, then the system displays the applicable categories and their content.
* **AC-161.2:** Given a category has no available observations, then it is omitted or shown as empty according to the interface design.
* **AC-161.3:** Given an observation is presented, then the system does not convert it into an unsupported guarantee about the property.

---

# 20. Agent Interaction

## FR-170 — Find Agent

### Acceptance Criteria

* **AC-170.1:** Given the user searches for an agent using supported criteria, then matching agent profiles are displayed where available.
* **AC-170.2:** Given an agent is selected, then the corresponding profile opens.
* **AC-170.3:** Given no agent matches, then the system displays an appropriate no-results state.

## FR-171 — Contact Agent

### Acceptance Criteria

* **AC-171.1:** Given an agent contact option is available, then the user can initiate contact.
* **AC-171.2:** Given required contact fields are missing or invalid, then the system identifies them.
* **AC-171.3:** Given a contact request is successfully submitted, then the system confirms submission.
* **AC-171.4:** Given submission fails, then the user is informed and can retry where appropriate.

## FR-172 — Agent Consultation

### Acceptance Criteria

* **AC-172.1:** Given consultation is offered, then the user can submit a consultation request.
* **AC-172.2:** Given a request is submitted successfully, then the system displays a confirmation.
* **AC-172.3:** Given a consultation time is not yet confirmed, then the system does not imply that an appointment is finalized.

## FR-173 — Agent Communication

### Acceptance Criteria

* **AC-173.1:** Given a supported communication channel is available, then the user can initiate communication through it.
* **AC-173.2:** Given communication is sent successfully, then the system provides the applicable success indication.
* **AC-173.3:** Given communication fails, then the system communicates the failure without falsely indicating delivery.

## FR-174 — Agent Information

### Acceptance Criteria

* **AC-174.1:** Given an agent profile is available, then the system displays the available profile information.
* **AC-174.2:** Given the user selects a contact or profile link, then the correct agent destination opens.
* **AC-174.3:** Given profile information is unavailable, then the system does not invent credentials, reviews, or professional details.

---

# 21. Buying Functionality

## FR-180 — Buyer Assistance

### Acceptance Criteria

* **AC-180.1:** Given a user accesses buyer services, then relevant buying resources and supported service options are displayed.
* **AC-180.2:** Given a user requests assistance, then the system routes them to the applicable contact or service workflow.
* **AC-180.3:** Given a service is not available in the user's market, then the limitation is communicated.

## FR-181 — Mortgage / Payment Information

### Acceptance Criteria

* **AC-181.1:** Given the user opens a supported payment calculator, then the required inputs are available.
* **AC-181.2:** Given valid inputs are submitted, then the system calculates and displays the estimated payment.
* **AC-181.3:** Given an input is invalid, then the system identifies the invalid field.
* **AC-181.4:** Given the payment is estimated, then the interface identifies it as an estimate and discloses relevant assumptions where provided.

## FR-182 — Buyer Resources

### Acceptance Criteria

* **AC-182.1:** Given buyer resources are available, then the user can access relevant educational content.
* **AC-182.2:** Given a resource is selected, then the correct content opens.
* **AC-182.3:** Given content is unavailable, then the system provides an appropriate response.

## FR-183 — Offer / Transaction Support

### Acceptance Criteria

* **AC-183.1:** Given the user is eligible for a supported transaction service, then the system provides the applicable next step.
* **AC-183.2:** Given agent assistance is required, then the system provides a means to connect with an agent.
* **AC-183.3:** Given a transaction action has not been completed, then the system does not represent the transaction as complete.

---

# 22. Selling Functionality

## FR-190 — Sell a Home

### Acceptance Criteria

* **AC-190.1:** Given a homeowner accesses the selling section, then the system presents available selling services and relevant entry points.
* **AC-190.2:** Given the homeowner selects a selling service, then the corresponding workflow opens.
* **AC-190.3:** Given the service is unavailable in the homeowner's location, then the system communicates that limitation.

## FR-191 — Home Valuation

### Acceptance Criteria

* **AC-191.1:** Given a valid supported address is entered, then the system displays an available home estimate.
* **AC-191.2:** Given the address cannot be matched, then the system requests correction or displays an appropriate error.
* **AC-191.3:** Given an estimate is returned, then it is labeled as an estimate and not a guaranteed sale price.

## FR-192 — Seller Consultation

### Acceptance Criteria

* **AC-192.1:** Given the user requests a selling consultation, then the system collects the required information.
* **AC-192.2:** Given the request is submitted, then a confirmation is displayed.
* **AC-192.3:** Given required information is invalid, then the system identifies the issue.

## FR-193 — Listing Services

### Acceptance Criteria

* **AC-193.1:** Given a seller begins a listing workflow, then the system guides them through the required steps.
* **AC-193.2:** Given required information is incomplete, then the system identifies the outstanding requirements.
* **AC-193.3:** Given a listing has not been published, then the system does not represent it as publicly active.

## FR-194 — Seller Resources

### Acceptance Criteria

* **AC-194.1:** Given seller resources are available, then the user can access them.
* **AC-194.2:** Given a resource is selected, then the relevant content opens.
* **AC-194.3:** Given a resource is unavailable, then the system communicates the issue.

---

# 23. Rental Search

## FR-200 — Rental Search

### Acceptance Criteria

* **AC-200.1:** Given the user selects Rent and enters a supported location, then rental results are displayed.
* **AC-200.2:** Given no rentals match, then the system displays an empty state.
* **AC-200.3:** Given the user opens a rental result, then the rental detail page is displayed.

## FR-201 — Rental Location

### Acceptance Criteria

* **AC-201.1:** Given a supported rental location is entered, then results correspond to that location.
* **AC-201.2:** Given multiple locations are supported in the rental search, then the system applies the selected locations.
* **AC-201.3:** Given a location is ambiguous, then the user can select the intended area.

## FR-202 — Rental Filters

### Acceptance Criteria

* **AC-202.1:** Given a rental price range is applied, then results follow the selected range.
* **AC-202.2:** Given bedroom, bathroom, property-type, pet, or other supported filters are selected, then results reflect those criteria.
* **AC-202.3:** Given multiple filters are active, then the results satisfy their combined conditions.
* **AC-202.4:** Given a filter is unsupported for the current search, then it is unavailable or clearly identified as inapplicable.

## FR-203 — Rental Detail

### Acceptance Criteria

* **AC-203.1:** Given a rental listing is opened, then the page displays available rent, location, property features, and rental terms.
* **AC-203.2:** Given rental-specific information is unavailable, then the system does not invent it.
* **AC-203.3:** Given the rental listing is no longer available, then the page reflects its current available status.

## FR-204 — Rental Contact

### Acceptance Criteria

* **AC-204.1:** Given a rental provides a contact option, then the user can initiate contact with the property manager or designated contact.
* **AC-204.2:** Given required fields are missing, then the system identifies them.
* **AC-204.3:** Given a request is submitted successfully, then the system confirms submission.
* **AC-204.4:** Given the listing has no supported contact route, then the system communicates that limitation.

## FR-205 — Rental Alerts

### Acceptance Criteria

* **AC-205.1:** Given a renter saves a search and enables alerts, then eligible matching rentals can trigger notifications.
* **AC-205.2:** Given alert preferences are changed, then subsequent notifications follow the updated settings.
* **AC-205.3:** Given alerts are disabled, then no new alerts are sent for that saved search.

---

# 24. Open Houses

## FR-210 — Open-House Discovery

### Acceptance Criteria

* **AC-210.1:** Given open-house listings exist within the active search, then the system identifies the applicable listings.
* **AC-210.2:** Given the user filters or searches for open houses, then results reflect the supported criteria.
* **AC-210.3:** Given no applicable open houses exist, then the system displays an appropriate empty state.

## FR-211 — Open-House Details

### Acceptance Criteria

* **AC-211.1:** Given an open house is scheduled, then its available date, time, property, and location are displayed.
* **AC-211.2:** Given an event changes, then the displayed information updates when available.
* **AC-211.3:** Given an event is canceled, then it is no longer represented as a confirmed upcoming event.

## FR-212 — Open-House Alerts

### Acceptance Criteria

* **AC-212.1:** Given open-house alerts are enabled, then applicable event notifications are sent.
* **AC-212.2:** Given an alert is opened, then it leads to the relevant property or event details.
* **AC-212.3:** Given alerts are disabled, then the user does not receive that alert category.

---

# 25. Market Information

## FR-220 — Market Trends

### Acceptance Criteria

* **AC-220.1:** Given market-trend data is available, then the system displays it for the relevant geographic area.
* **AC-220.2:** Given trends cover a defined period, then the period is identifiable.
* **AC-220.3:** Given the data is unavailable, then the system does not substitute unsupported values.

## FR-221 — Local Statistics

### Acceptance Criteria

* **AC-221.1:** Given local statistics are displayed, then the associated location and applicable period are identifiable.
* **AC-221.2:** Given the user changes the selected location, then the statistics update to the new area where data exists.
* **AC-221.3:** Given a statistic is an estimate or derived measure, then it is labeled or explained accordingly.

## FR-222 — Market Reports

### Acceptance Criteria

* **AC-222.1:** Given a market report is available, then the user can open it.
* **AC-222.2:** Given the report is selected from a particular market, then the report corresponds to that market.
* **AC-222.3:** Given a report is unavailable, then the system provides an appropriate message.

## FR-223 — Home Reports

### Acceptance Criteria

* **AC-223.1:** Given a user is eligible for a home report, then the report or subscription option is available.
* **AC-223.2:** Given a report is generated or updated, then the system makes the available information accessible.
* **AC-223.3:** Given the user is not eligible or data is unavailable, then the system communicates the limitation.

---

# 26. Account Management

## FR-230 — Registration

### Acceptance Criteria

* **AC-230.1:** Given a visitor provides valid required registration information, then the system creates an account according to the supported registration process.
* **AC-230.2:** Given required fields are missing or invalid, then the system identifies the errors.
* **AC-230.3:** Given the account cannot be created, then the system communicates the failure without displaying a false success state.

## FR-231 — Login

### Acceptance Criteria

* **AC-231.1:** Given valid credentials or a supported authentication method, then the user can sign in.
* **AC-231.2:** Given invalid credentials, then access is denied and an appropriate error is displayed.
* **AC-231.3:** Given successful authentication, then the user can access their permitted account features.

## FR-232 — Logout

### Acceptance Criteria

* **AC-232.1:** Given an authenticated user selects Sign Out, then the active session is ended according to the authentication design.
* **AC-232.2:** Given sign-out succeeds, then the user is returned to an appropriate public state.
* **AC-232.3:** Given the user attempts to access a protected page after signing out, then authentication is required.

## FR-233 — Password Management

### Acceptance Criteria

* **AC-233.1:** Given a user initiates a supported password-recovery process, then the system guides them through the required verification steps.
* **AC-233.2:** Given a password change is successful, then the system confirms the change.
* **AC-233.3:** Given verification fails, then the system does not permit an unauthorized password change.

## FR-234 — Profile Management

### Acceptance Criteria

* **AC-234.1:** Given a user edits supported profile fields, then valid changes can be saved.
* **AC-234.2:** Given the user revisits the profile, then saved values are displayed.
* **AC-234.3:** Given an invalid value is submitted, then the system identifies the issue and prevents invalid data from being saved.

## FR-235 — Notification Preferences

### Acceptance Criteria

* **AC-235.1:** Given a user changes notification preferences, then the system saves the new settings.
* **AC-235.2:** Given the user signs in again, then the saved preferences remain in effect.
* **AC-235.3:** Given a preference cannot be changed, then the system explains the limitation.

---

# 27. My Redfin Dashboard

## FR-240 — User Dashboard

### Acceptance Criteria

* **AC-240.1:** Given an authenticated user opens their dashboard, then the system displays the account features available to that user.
* **AC-240.2:** Given the user has saved properties or searches, then applicable items are accessible from the dashboard.
* **AC-240.3:** Given the user has no saved items, then the dashboard displays an appropriate empty state.
* **AC-240.4:** Given a dashboard item is selected, then the correct destination opens.

---

# 28. My Home / Property Management

## FR-250 — Claim Home

### Acceptance Criteria

* **AC-250.1:** Given a user initiates a supported home-claim process, then the system collects the required information.
* **AC-250.2:** Given verification is required, then the system does not grant ownership-related access until the required verification succeeds.
* **AC-250.3:** Given the claim cannot be completed, then the system communicates the reason or next step where available.

## FR-251 — Home Information

### Acceptance Criteria

* **AC-251.1:** Given a property is associated with the user's account, then available home information is displayed.
* **AC-251.2:** Given a property is not associated with the account, then restricted home-management information is not exposed.
* **AC-251.3:** Given information is missing, then the system does not invent property details.

## FR-252 — Home Value

### Acceptance Criteria

* **AC-252.1:** Given an estimate is available for the associated home, then the user can view it.
* **AC-252.2:** Given the estimate is unavailable, then the system communicates that state.
* **AC-252.3:** Given the estimate is displayed, then it is identified as an estimate.

## FR-253 — Home Updates

### Acceptance Criteria

* **AC-253.1:** Given relevant home updates are available and enabled, then the user can receive them.
* **AC-253.2:** Given the user disables a supported update category, then future notifications in that category are suppressed.
* **AC-253.3:** Given an update is displayed, then it is associated with the correct property.

---

# 29. Search by School

## FR-260 — School Search

### Acceptance Criteria

* **AC-260.1:** Given a supported school name or location is entered, then matching school results are displayed where available.
* **AC-260.2:** Given multiple schools match, then the user can identify the intended school.
* **AC-260.3:** Given no school matches, then the system displays an appropriate no-results state.

## FR-261 — School-Related Property Search

### Acceptance Criteria

* **AC-261.1:** Given a school or school area is selected, then the system displays properties associated with that selection where supported.
* **AC-261.2:** Given the user changes the school selection, then the property results update.
* **AC-261.3:** Given school-area data is unavailable, then the system communicates the limitation.

## FR-262 — School Information

### Acceptance Criteria

* **AC-262.1:** Given school information is available, then the system displays the available details.
* **AC-262.2:** Given ratings or other third-party information are displayed, then their source or attribution is provided where applicable.
* **AC-262.3:** Given information is unavailable, then no unsupported rating or detail is displayed.

---

# 30. Agent Search

## FR-270 — Agent Search

### Acceptance Criteria

* **AC-270.1:** Given the user enters supported agent-search criteria, then matching agent results are displayed.
* **AC-270.2:** Given a result is selected, then the corresponding agent profile opens.
* **AC-270.3:** Given no agents match, then an appropriate empty state is displayed.

## FR-271 — Agent Location

### Acceptance Criteria

* **AC-271.1:** Given a location is selected, then results reflect the supported geographic scope.
* **AC-271.2:** Given the location changes, then the results update.
* **AC-271.3:** Given the location cannot be resolved, then the system asks for a valid location.

## FR-272 — Agent Profile

### Acceptance Criteria

* **AC-272.1:** Given an agent profile is available, then the system displays the available profile information.
* **AC-272.2:** Given profile links are provided, then they lead to the correct destinations.
* **AC-272.3:** Given information is not available, then it is not fabricated.

## FR-273 — Agent Contact

### Acceptance Criteria

* **AC-273.1:** Given contact functionality is available, then the user can submit a contact request.
* **AC-273.2:** Given required information is invalid, then the system identifies the issue.
* **AC-273.3:** Given the request is submitted successfully, then confirmation is displayed.

---

# 31. Search History

## FR-280 — Recent Searches

### Acceptance Criteria

* **AC-280.1:** Given recent-search functionality is enabled, then applicable previous searches are displayed.
* **AC-280.2:** Given a recent search is selected, then the corresponding search is restored.
* **AC-280.3:** Given no recent searches exist, then the system displays an appropriate empty state.
* **AC-280.4:** Given search history is cleared or removed through a supported control, then the removed items no longer appear in that history.

## FR-281 — Reuse Search

### Acceptance Criteria

* **AC-281.1:** Given a user selects a recent search, then the system restores its supported location and criteria.
* **AC-281.2:** Given the underlying listing inventory has changed, then the restored search displays currently available results rather than a stale snapshot unless explicitly presented as historical.
* **AC-281.3:** Given a previous location is no longer resolvable, then the system communicates the issue.

---

# 32. Mobile Experience

## FR-290 — Mobile Web

### Acceptance Criteria

* **AC-290.1:** Given Redfin is opened in a supported mobile browser, then the interface adapts to the available screen size.
* **AC-290.2:** Given a user performs a core search or opens a listing, then the primary controls and content remain usable.
* **AC-290.3:** Given the viewport changes, then content does not become inaccessible due to unintended layout overflow.

## FR-291 — iOS Application

### Acceptance Criteria

* **AC-291.1:** Given the supported iOS application is installed and opened, then its supported core functions are accessible.
* **AC-291.2:** Given the user searches, opens a listing, or saves a property, then the action produces the expected result.
* **AC-291.3:** Given a supported app notification is selected, then it opens the relevant destination.

## FR-292 — Android Application

### Acceptance Criteria

* **AC-292.1:** Given the supported Android application is installed and opened, then its supported core functions are accessible.
* **AC-292.2:** Given the user searches, opens a listing, or saves a property, then the action produces the expected result.
* **AC-292.3:** Given a supported app notification is selected, then it opens the relevant destination.

## FR-293 — Mobile Search

### Acceptance Criteria

* **AC-293.1:** Given a mobile user searches for properties, then they can enter a location and apply supported filters.
* **AC-293.2:** Given a user opens a listing, then property details and available photographs are accessible.
* **AC-293.3:** Given a user saves a property or search, then the saved item is associated with their account when authenticated.
* **AC-293.4:** Given a user shares a property, then the supported mobile sharing mechanism is available.

---

# 33. Navigation

## FR-300 — Primary Navigation

### Acceptance Criteria

* **AC-300.1:** Given a user opens the primary navigation, then the available major service destinations are presented.
* **AC-300.2:** Given a navigation item is selected, then the correct page or workflow opens.
* **AC-300.3:** Given the user is on a mobile device, then navigation remains accessible through the mobile interface.

## FR-301 — Contextual Navigation

### Acceptance Criteria

* **AC-301.1:** Given a user moves from search results to a listing, then the correct listing is opened.
* **AC-301.2:** Given the user returns to results, then the active search context is retained where supported.
* **AC-301.3:** Given a user navigates from a listing to a tour, favorite, or agent-contact workflow, then the selected property is associated with the action.

---

# 34. Property Data Integrity

## FR-310 — Listing Data

### Acceptance Criteria

* **AC-310.1:** Given listing information is displayed, then it corresponds to the associated listing record available to Redfin.
* **AC-310.2:** Given information comes from a third-party or MLS source, then applicable attribution or disclaimers are displayed.
* **AC-310.3:** Given data is missing, then the system does not substitute an invented value.

## FR-311 — Data Updates

### Acceptance Criteria

* **AC-311.1:** Given updated listing data is received, then the system reflects the update according to its data-refresh behavior.
* **AC-311.2:** Given a listing's price or status changes, then applicable search and detail views reflect the update when refreshed.
* **AC-311.3:** Given an update cannot be retrieved, then the system does not falsely claim that the displayed data is current.

## FR-312 — Missing Information

### Acceptance Criteria

* **AC-312.1:** Given a property field is unavailable, then the system displays an appropriate unavailable state or omits the field.
* **AC-312.2:** Given a value is estimated, then it is distinguishable from a directly reported value.
* **AC-312.3:** Given data sources conflict or are incomplete, then the system follows its defined source-handling rules and does not present unsupported certainty.

---

# 35. Notifications Delivery

## FR-320 — Email Notifications

### Acceptance Criteria

* **AC-320.1:** Given email notifications are enabled and an eligible event occurs, then the system initiates delivery to the user's configured email address.
* **AC-320.2:** Given the email address requires verification, then the system follows the supported verification process.
* **AC-320.3:** Given delivery fails or cannot be confirmed, then the system does not claim confirmed receipt.

## FR-321 — Push Notifications

### Acceptance Criteria

* **AC-321.1:** Given push notifications are enabled and permission is granted, then eligible notifications can be delivered to the supported device.
* **AC-321.2:** Given device permission is denied, then the system respects that setting.
* **AC-321.3:** Given a push notification is selected, then it opens the corresponding supported destination.

## FR-322 — Text Notifications

### Acceptance Criteria

* **AC-322.1:** Given SMS notifications are supported for the user and event, then the system follows the applicable opt-in and delivery process.
* **AC-322.2:** Given consent is required and has not been provided, then the system does not send the applicable text notification.
* **AC-322.3:** Given a user opts out, then subsequent messages follow the applicable opt-out behavior.

## FR-323 — Notification Frequency

### Acceptance Criteria

* **AC-323.1:** Given a supported frequency is selected, then notifications follow that setting.
* **AC-323.2:** Given the user changes frequency, then subsequent notifications use the updated preference.
* **AC-323.3:** Given a frequency option is unavailable, then it is not offered as an active choice.

## FR-324 — Notification Categories

### Acceptance Criteria

* **AC-324.1:** Given notification categories are configurable, then the user can manage each supported category.
* **AC-324.2:** Given a category is disabled, then notifications in that category are suppressed.
* **AC-324.3:** Given a category is enabled, then eligible notifications can be delivered subject to the user's other settings.

---

# 36. Content and Resources

## FR-330 — Real-Estate Education

### Acceptance Criteria

* **AC-330.1:** Given educational content is available, then the user can access it from the relevant section.
* **AC-330.2:** Given the user selects a content item, then the corresponding article or resource opens.
* **AC-330.3:** Given the content is unavailable, then the system provides an appropriate message.

## FR-331 — Market Content

### Acceptance Criteria

* **AC-331.1:** Given market articles or reports are available, then the user can browse and open them.
* **AC-331.2:** Given an article refers to a particular market or period, then that context is identifiable.
* **AC-331.3:** Given a content link is unavailable, then the system handles the error gracefully.

## FR-332 — Local Content

### Acceptance Criteria

* **AC-332.1:** Given local content is available for a selected area, then the system displays content relevant to that area.
* **AC-332.2:** Given the user changes the selected area, then local content updates where supported.
* **AC-332.3:** Given no local content is available, then the system displays a suitable fallback.

---

# 37. Customer Support

## FR-340 — Help Center

### Acceptance Criteria

* **AC-340.1:** Given a user opens the Help Center, then available support topics are displayed.
* **AC-340.2:** Given a support topic is selected, then the relevant help content opens.
* **AC-340.3:** Given the Help Center is unavailable, then the system provides an appropriate error state.

## FR-341 — Help Search

### Acceptance Criteria

* **AC-341.1:** Given a user enters a help query, then relevant support results are displayed where available.
* **AC-341.2:** Given a result is selected, then the corresponding help article opens.
* **AC-341.3:** Given no results match, then the system communicates that no matching help content was found.

## FR-342 — Customer Contact

### Acceptance Criteria

* **AC-342.1:** Given a support contact channel is available, then the user can access it.
* **AC-342.2:** Given a support request requires specific information, then the system identifies the required fields.
* **AC-342.3:** Given a request is submitted successfully, then the system confirms submission.
* **AC-342.4:** Given the request cannot be submitted, then the system communicates the failure.

---

# 38. Error Handling

## FR-350 — Invalid Search

### Acceptance Criteria

* **AC-350.1:** Given a search input cannot be processed, then the system displays a clear validation or error message.
* **AC-350.2:** Given the input can be corrected, then the user can edit it and retry.
* **AC-350.3:** Given the input is ambiguous, then the system requests clarification rather than silently selecting an unintended location.

## FR-351 — No Results

### Acceptance Criteria

* **AC-351.1:** Given a valid search returns no matches, then the system displays a no-results state.
* **AC-351.2:** Given filters may be restricting results, then the user can revise or clear filters.
* **AC-351.3:** Given alternative locations or criteria are available, then the interface may offer relevant ways to broaden the search.

## FR-352 — Unavailable Property

### Acceptance Criteria

* **AC-352.1:** Given a listing is removed or unavailable, then the system displays the appropriate status or unavailable state.
* **AC-352.2:** Given the listing is no longer active, then the system does not present it as an active listing.
* **AC-352.3:** Given historical information remains available, then it may be displayed as historical rather than current listing information.

## FR-353 — Service Failure

### Acceptance Criteria

* **AC-353.1:** Given a service request fails, then the system displays an appropriate error state.
* **AC-353.2:** Given retry is supported, then the user can retry the operation.
* **AC-353.3:** Given a request fails, then the system does not display a success confirmation.
* **AC-353.4:** Given the failure affects only one feature, then other usable page functionality remains available where possible.

## FR-354 — Authentication Failure

### Acceptance Criteria

* **AC-354.1:** Given authentication fails, then access to the protected operation is denied.
* **AC-354.2:** Given the user enters invalid credentials, then an appropriate error is displayed.
* **AC-354.3:** Given authentication is required for an action, then the user is directed to the supported sign-in flow.
* **AC-354.4:** Given authentication succeeds, then the user can return to the intended action where supported.
