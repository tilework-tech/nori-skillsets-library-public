---
name: designing-frontend-systems
description: Use when designing a frontend system architecture. For example, use this skill when thinking about how to implement frontend state, how to integrate with a backend API, or how to wire together multiple UI components.
---

<required>
CRITICAL. Add the following steps to your task list:

1. Read the system design principles below as context for any other tasks.

</required>

# System Design Principles

<system-reminder> This system design assumes vue components, but the same principles should apply across many kinds of codebases. </system-reminder>

Folder structure:
```
App.vue  # Entry point.
router.ts  # Maps between routes and pages using vue-router or equivalent.
pages/  # Individual page wrappers.
  Foo.vue
features/  # All business logic lives here.
  foo/
    FooPanel.vue
    fooStateStore.ts  # Every feature has a store that tracks state.
    fooUIStore.ts  # Every feature may optionally have a store that tracks ui state.
  bar/
    barComposable.ts
    BarModal.vue
    barStateStore.ts
    barUIStore.ts
providers/  # Third party integrations.
  firebase.ts
  sqlite.ts
api/  # Backend integrations.
  foo.ts
  bar.ts
components/  # All components that have NO business logic. Could easily be pulled out of the application and used anywhere else.
  TreeNode.vue
  TitleCard.vue
style.css
```

pages:
- Pages are lightweight wrappers. All actual logic lives in features.

features:
- Features are split between folders that are semantically tied to a specific coherent application behavior.
- Features can apply across pages. For example, a navigation-bar feature may live in several pages, or in App.vue (i.e. across all pages)
- Features contain all business logic. Any components or logic that is unique to the application should be in a feature.
- Components inside a feature should not use prop drilling or events. Instead, they must interact with each other through shared state for that feature in pinia stores.
- Most features will have two pinia stores: a state store and a ui store.
- The state store is the ground truth for all of the application state. Anything that interacts with the backend or api should go through the state store.
- The ui store is the ground truth for all of the UI state. Toggles, loading states, notification messages, anything that is just for one component to communicate with other components should route through the ui store.
- Components inside features should not call the API or providers directly. They should always route through a store.

providers:
- Providers are singleton classes that wrap third party services. Common providers include auth, databases, cloud services.
- Each provider should be instantiated once on startup.
- Providers are 'dumb'. They do not care about business logic. Database providers should expose basic CRUD functions. Other providers should be as unopinionated as possible.

api:
- Each file in the api folder must correspond to some backend behavior or persisted type.
- These files should export types that match backend request/response types 1:1.

components:
- Components in the components/ folder are the opposite of features. These do not have any business logic.
- Components should exclusively communicate using props and events, and not use stores.
- Components should be entirely agnostic to the project. They can be dropped into a new project without any changes.
