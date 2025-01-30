# State Management Strategy for Kryptt

This document outlines the state management strategy for the Kryptt application.

## Local State

Local state will be managed within individual components using React's built-in state management capabilities.  This approach is suitable for component-specific data that doesn't need to be shared across the application.  Examples include form inputs and temporary UI state.

## Global State

Global state will be managed using Zustand.  Zustand provides a simple and efficient way to manage state that needs to be accessible across multiple components. This will be used for application-wide data such as user authentication status, portfolio data, and application settings.

## Server State

Server state, such as data fetched from the Alpaca API, will be managed using React Query.  React Query provides features like caching, background updates, and optimistic updates, improving the user experience and performance.

## Persistence

User preferences will be persisted using local storage.  This allows settings to be preserved across user sessions.
