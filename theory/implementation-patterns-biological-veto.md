# Implementation Patterns: The Biological Veto in AI Agents

## Abstract

This Request for Comments (RFC) defines standard architectural patterns within the Thermodynamic Equilibrium Operations (TEO) framework for implementing safety constraints on autonomous AI systems. The objective is to prevent frictionless, unconstrained scaling of agentic execution loops by enforcing structural boundaries, collectively referred to as the Biological Veto. The patterns outlined below establish concrete, code-level constraints to ensure deterministic control over non-deterministic systems.

## Architectural Constraints

### 1. Action Budgets (Thermodynamic Limits)

To prevent runaway execution loops, agent state machines must be structurally constrained by pre-allocated resource limits per session state. These limits act as hard thermodynamic bounds on the agent's capacity to induce state changes.

*   **Token Quotas:** Strict, non-replenishable limits are enforced on the total aggregate tokens generated and processed per session instance.
*   **API Invocation Caps:** Agents operate from a predefined, immutable budget of permissible third-party network requests, file I/O operations, or database mutations. Exceeding this budget automatically triggers an execution halt.
*   **Time-to-Live (TTL) Decay:** The execution scope decays predictably. Sessions have a strict maximum runtime, requiring deliberate, external state renewal to continue operations.
*   **Implementation Pattern:** Deploy a centralized `BudgetManager` middleware that intercepts, validates, and tracks all output commands from the agent. When resource metrics exceed threshold parameters, the middleware returns a deterministic failure code (e.g., HTTP 429) directly to the execution loop, forcing a halt.

### 2. Meaningful Friction (The Veto)

Frictionless autonomous execution is an architectural anti-pattern for critical, state-altering mutations. The system must introduce deliberate latency via UI/UX patterns that necessitate conscious, physical verification.

*   **Hardware Validation:** The execution of high-privilege commands strictly requires physical human interaction, such as a YubiKey capacitive touch or a biometric hardware passkey.
*   **Asynchronous Commits:** Destructive or high-impact systemic actions enter an asynchronous staging queue, requiring out-of-band user approval rather than executing in immediate real-time.
*   **Cryptographic Signatures:** Human approvals are treated as cryptographically signed payloads. The backend execution engine explicitly rejects unsigned mutation requests originating from the automated agent layer.
*   **Implementation Pattern:** The execution engine halts the current thread and emits a `HumanVerificationRequired` event to the client interface. The state machine remains suspended indefinitely until a cryptographically verified external payload is received.

### 3. The Edge Gatekeeper

System integrity relies on a strict topological separation between non-deterministic cloud generation models and deterministic local execution environments.

*   **Local Validation:** A standalone, deterministic compiled binary runs explicitly on the network edge or directly on the user's host device.
*   **Action Filtering:** This gatekeeper evaluates all incoming instruction directives from the cloud-based LLM inference instance against a predefined, immutable local schema of permissible functions.
*   **Sandboxing:** Approved functions are executed within isolated, low-privilege containers. Arbitrary code execution or system-level directives are outright rejected at the boundary.
*   **Implementation Pattern:** The cloud LLM outputs commands strictly as JSON-RPC payloads. The edge binary parses the JSON, validates arguments against static type mappings, and executes the routines via restricted OS-level system calls, functioning as an immutable firewall against prompt injection or logic drift.

## Open Source Resilience and Human Agency

Publishing these architectural constraints as distributed, open-source patterns provides a structurally superior mechanism for preserving human agency. Isolated, centralized AI monoliths introduce systemic single points of failure, relying entirely on the opaque self-regulation of corporate providers to enforce alignment. Conversely, standardizing biological vetoes and thermodynamic quotas as an open operational protocol democratizes the enforcement of computational limits. By embedding these friction-inducing patterns directly into the public software engineering commons, we establish decentralized cryptographic and structural guarantees that autonomous agents remain strictly subordinate to human consensus, regardless of the underlying foundation model's capability edge.
