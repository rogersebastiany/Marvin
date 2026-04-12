# MCP

Model Context Protocol. O(1) indirect addressing for external [[Context]] via gRPC. The open gate between AI and data.

---

## Definition

MCP places procedures directly on stdin/stdout via gRPC. It is stream, not async. For the AI, accessing a log on the Frankfurt server or a table in the local database has the same cognitive "cost." It is O(1), as if it were RAM.

"The model does not need to 'search' for how to access -- the interface is already mapped."

## Without MCP vs With MCP

**Without**: integrating an external tool requires creating APIs, dealing with complex authentication and latency. Each integration is a project.

**With**: context (logs, DB, metrics, [[Tool|tools]]) exposed via gRPC. Indirect addressing -- the model points to the context, it does not copy.

## The Open Gate

MCP is the open gate between AI and context. The gate itself has no security -- it is a raw pipe. Security is in the surrounding terrain: VPN, mTLS, VPC, IAM, WAF, Cognito.

## Enabler of the Ontology

MCP is what makes complete [[Ontology]] viable in real time. Without MCP, accessing each external context would have variable latency, different authentication, incompatible formats. With MCP, everything is O(1), everything is stream, everything is standardized.

It is the infrastructure component that transforms theory (complete ontology) into practice (instant access to all context).

---

Related to: [[Tool]], [[Context]], [[Agent]], [[Ontology]], [[RAG]]
