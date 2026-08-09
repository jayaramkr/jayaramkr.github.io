---
layout: default
permalink: /research/
title: Research
subtitle: Twenty years of work on distributed systems, organized by theme rather than by date. Newest first.
description: Research themes of Jayaram K Radhakrishnan — agentic memory, LLM agents, federated learning, deep learning platforms, cloud elasticity and trust, and event-based systems.
---
{%- comment -%}
All theme lookups are hoisted here on purpose. A whitespace-trimming Liquid tag
placed directly under a Markdown heading swallows the blank line after it and
pulls the following paragraph into the heading.
{%- endcomment -%}
{%- assign t_memory = site.data.themes | where: "id", "agentic-memory" | first -%}
{%- assign t_agents = site.data.themes | where: "id", "llm-agents" | first -%}
{%- assign t_flpriv = site.data.themes | where: "id", "fl-privacy" | first -%}
{%- assign t_flpart = site.data.themes | where: "id", "fl-participation" | first -%}
{%- assign t_dl = site.data.themes | where: "id", "dl-platforms" | first -%}
{%- assign t_cloud = site.data.themes | where: "id", "cloud-trust" | first -%}
{%- assign t_events = site.data.themes | where: "id", "events-pubsub" | first -%}

The subject has changed every few years — event correlation, then cloud elasticity, then
deep learning infrastructure, then federated learning, now agents. The question underneath
has not. Each time, a new class of computation arrived that people wanted to run in
production, and each time the gap was the same: the runtime could not see what the
application was actually doing, so it made bad decisions about resources, correctness, and
trust. The work has consistently been about closing that gap in the middleware layer, so
that neither the application above nor the infrastructure below has to be rewritten.

## Agentic memory and self-improving agents
<span class="theme-span">{{ t_memory.span }}</span>

Agents built on large language models have amnesia. The model underneath is stateless, so an
agent that solved a problem yesterday re-derives it today, repeats the detour it already
backed out of once, and loses the context that made the previous run work. General-purpose
memory systems store conversational facts — what was said, what was decided — but an agent's
most valuable experience is procedural: which sequence of calls worked, which failed and why,
and what the cheaper path would have been. My current work treats that experience as
something to be extracted, structured, and then retrieved under an explicit budget.

**Trajectory-informed memory generation** turns raw execution traces into typed, reusable
guidance. A pipeline parses an agent's reasoning into analytical, planning, validation and
reflection steps; traces failures backwards to separate immediate causes from root causes;
and emits three kinds of tip — strategy tips from clean successes, recovery tips from
failure-then-recovery sequences, and optimization tips from successes that took too long.
Each tip carries a trigger condition, a priority, and a pointer back to the trajectory that
produced it, so anything in memory can be traced to the run that justified it. Tips are
generalized away from the specific entities that produced them, then clustered and
consolidated so the store does not simply grow without bound. On the AppWorld benchmark,
subtask-level tips with model-guided retrieval raised scenario goal completion from 50.0% to
64.3%, and on the hardest tasks from 19.1% to 47.6%. The negative result matters as much as
the gain: a too-restrictive retrieval setting pushed the agent *below* the no-memory
baseline, because irrelevant tips actively interfere. Selection quality, not storage
capacity, is the binding constraint. These techniques are being applied to IBM's CUGA agent
platform.

**VOILA** attacks the read side of the same problem. Multimodal agents typically run at a
fixed input fidelity, but their data lives across storage tiers — a thumbnail on the device,
full resolution in cloud object storage, an archive tier that costs seconds to touch.
Retrieval cost is paid *before* any model runs, so choosing between models after the fact is
already too late. VOILA predicts, from the question text alone, how likely a correct answer
is at each available fidelity, calibrates those predictions, and escalates from the cheapest
representation upward only while the expected gain still exceeds the cost of acquiring it.
Across five datasets and six vision-language models spanning 7B to 235B parameters, this cut
acquisition cost by 50–60% while retaining 90–95% of full-resolution accuracy, at a selection
overhead of 0.45 ms against inference times measured in seconds. Two findings shaped the
design: model confidence is an unreliable signal of whether the context was sufficient, and
scaling the model does not compensate for visual information that was never retrieved.

The through-line is that the object worth optimizing is the context an agent is given, not
the weights it runs on. Both systems wrap an unmodified frozen model and decide what is worth
writing down, and what it is worth paying to read back.

{% include theme_items.html theme=t_memory %}

## LLM agents for enterprise automation
<span class="theme-span">{{ t_agents.span }}</span>

Enterprise automation is where agents meet a catalog. A business process is not free-form
generation: it has to call the right API from a specific inventory, pass real parameters, and
emit something a runtime will actually execute. Across this group of papers one finding
recurs — retrieval quality, not model size, is the dominant lever.

**A conversational assistant framework for automation** starts from a blunt observation about
low-code tools: low-code does not imply low effort. One representative flow took roughly 45
interface clicks to assemble. The framework replaces that with an event-driven architecture
of pluggable agents — each subscribing to events, each declaring in plain text what it does —
and an orchestrator that routes natural-language requests using only those descriptions.
Because agents can trigger one another, compositions form at runtime instead of being wired
in advance. Routing across seven agents reached 92.9% accuracy over 150 utterances with the
strongest model tested. Two negative results are load-bearing: zero-shot prompting cannot
generate workflows at all, and a random skill retriever loses badly to top-k retrieval no
matter how large k gets.

**FLOW-BENCH** turned that system's core into something reproducible. Asking a model to emit
BPMN directly is hopeless — in this dataset the BPMN form runs on average 25 times longer than
the equivalent Python, 3,151 characters against 148 in one case. The generator instead emits
a constrained Python intermediate representation — assignments, conditionals, loops, calls —
which is compiled deterministically into BPMN. The benchmark is 101 incremental build-step
tests drawn from real App Connect and Zapier templates, released publicly, and the approach
shipped as a technical preview in watsonx Orchestrate's Unified Automation Builder.

**OptiSeq** addresses a failure mode the systems papers surfaced but did not solve. In-context
learning is order-sensitive: the same examples in a different sequence produce different
answers, varying accuracy by roughly 12 points on API generation in the paper's own
sensitivity analysis. Existing fixes assume a validation set and offline tuning, which a
deployed product does not have. OptiSeq permutes the examples, generates a candidate output
for each ordering, then *removes the examples* and rescores each candidate against the
instruction alone — the step that makes right and wrong candidates separable, which raw
in-context log probabilities do not. It gains 5.5 to 10.5 percentage points over random
selection, top-k, and two stronger baselines across five datasets and five models, and
batching keeps the factorial search to roughly the cost of two sequential calls.

**Automating security policies** shows the pattern generalizes beyond workflows. A high-level
mitigation directive is decomposed into discrete tasks by one model; a second generates the
API sequence for each task from retrieved documentation. Grounding in retrieved specifications
was worth about 22 F1 points on average, and 37 for the largest model — with retrieval, a
small model matched an ungrounded large one. The authors also report a hypothesis of their own
that failed: they expected the ungrounded baseline to produce nothing usable, and it did not,
suggesting parts of the API surface are already memorized.

{% include theme_items.html theme=t_agents %}

## Federated learning: privacy and secure aggregation
<span class="theme-span">{{ t_flpriv.span }}</span>

Federated learning promises that sharing model updates instead of data is private for free. It
is not. Model-inversion and membership-inference attacks reconstruct training data from
plaintext gradients, which makes the aggregator — the one place where every participant's
update converges — the weak point of the whole arrangement. Two strands of this work attack
it: one on confidentiality, one on the cost and scale of aggregation itself.

**MYSTIKO** buys confidentiality with cryptography. A cloud-mediated coordinator generates a
per-job keypair, distributes the public key to learners, and holds the private key itself, so
it can decrypt only the fully aggregated gradient and never an individual contribution. Three
protocols aggregate over ciphertext: a ring, a failure-resilient broadcast variant, and a
chunked ring all-reduce. Against the secure-multiparty alternative it is up to 6.1× faster in
total synchronization time, and unlike differential privacy it adds no noise, so accuracy is
untouched — the paper measures noise addition dropping accuracy on one benchmark from 98.3% to
88.9% at the tightest privacy budget tested. It is also honest about what homomorphic
encryption still costs: training runs on GPUs while the cryptography runs on CPUs, and
synchronization stays large relative to epoch time.

**DeTA** removes the single trusted point altogether, and then assumes the obvious defense
fails anyway. Wrapping an aggregator in confidential computing is the natural fix, but trusted
hardware has its own disclosed vulnerabilities, so DeTA layers three mechanisms rather than
relying on one. Each party splits its update at parameter granularity across several
aggregators, so none sees a whole update or even the model architecture; parameters are
permuted within each partition and reseeded every round; and parties verify each aggregator by
hardware attestation before sending anything. The security evaluation assumes an attacker has
already breached *every* protected aggregator. Under that assumption, reconstruction attacks
that recovered recognizable images 66.6% and 83.7% of the time drop to zero. Overheads run
from 0.04× to 0.45×, and accuracy holds or improves. The shuffling component shipped into
IBM's open-source federated learning library.

The second strand is about what aggregation costs to run. Production federated learning wastes
enormous resources on always-on aggregators that idle while intermittent participants train —
in one measured round, idle 71.4% of the time. **Adaptive aggregation** makes aggregators
stateless enough to run as ephemeral serverless functions chained through message queues,
forming a *logical* tree with no physical overlay to build, heal, or reconfigure. It cuts
resources and cost by more than 90% against a static tree while staying within 4% of its
latency, and reconfigures 2.5–4.6× faster when parties join mid-job. **Just-in-time
aggregation** asks the complementary question of *when*: because minibatch and epoch times are
near-constant and scale linearly, a party's arrival time can be predicted, and aggregation
deferred until just late enough to finish as the last update lands. That saves 60% or more
over eager aggregation with negligible latency cost.

{% include theme_items.html theme=t_flpriv %}

## Federated learning: participation, scale, and adaptation
<span class="theme-span">{{ t_flpart.span }}</span>

Most federated learning algorithms select a subset of participants each round, and that
selection is usually random. Under non-IID data, random selection is actively harmful: whole
label classes can go unrepresented for many consecutive rounds, so the global model is biased
against exactly the cases that matter — the arrhythmia class in an ECG dataset, the malignant
label in a skin-lesion dataset.

**FLIPS** makes label distribution the basis for selection. Parties report only the
distribution of their labels, never their data; the aggregator clusters parties on those
vectors and then picks round-robin across clusters, so every cluster is represented every
round and every party gets a fair share of participation over time. Stragglers are handled by
over-provisioning from the clusters that produced the previous round's stragglers. Because a
label distribution is itself sensitive, the clustering and selection run inside a hardware
enclave that parties verify by attestation — a design that costs about 5% over running it in
the clear. Against random selection and three published selection strategies, FLIPS speeds up
convergence by 1.2× to 2.9× and improves terminal accuracy by 5 to 30 percentage points, with
the largest gains where label skew is worst. The most interesting result is diagnostic:
gradient-based clustering performs no better than random on two of the medical datasets,
because gradients do not recover label structure, and tier-based selection cannot isolate the
parties holding rare labels at all.

**ShiftEx** takes up the problem FLIPS explicitly left open — what happens when the
distributions move. Real deployments are streaming, and party data drifts: the inputs change
character, the label mix shifts, and a single global model degrades while aggregation across
divergent parties actively transfers the wrong knowledge. ShiftEx detects both kinds of drift
locally, from summary statistics rather than raw data, and assigns parties to a dynamically
maintained pool of expert models. Experts are created only when no existing one matches,
reused when one does, and periodically merged when they converge, which keeps the pool from
proliferating. Assignment happens per party rather than per input, so no gating network is
needed and inference stays local. It improves accuracy by 5.5 to 12.9 percentage points and
adapts 22–95% faster than the strongest baselines, recovering in single-digit rounds on
datasets where the alternatives never recover at all. FLIPS runs inside it, keeping each
expert's training cohort label-balanced.

Here too the sharpest finding is about a baseline rather than the system: utility-based
selection shows the *smallest* initial accuracy drop under distribution shift, which reads as
robustness but is closer to its opposite — the selection masks the change and prevents the
model from adapting to it.

Work is underway to apply this in assisted-living settings, where wearable and ambient sensing
produce exactly the kind of skewed, drifting, privacy-constrained data these systems were
designed for.

{% include theme_items.html theme=t_flpart %}

## Platforms for large-scale deep learning
<span class="theme-span">{{ t_dl.span }}</span>

The deep learning stack and the cloud stack were each designed without the other in mind.
Frameworks assume stable, dedicated hardware and handle no faults; container orchestrators
know nothing about gang scheduling, GPU topology, or what it means for a training job to be
"storing results." The argument across this work is that the fix belongs in middleware — so
that neither the frameworks nor the cluster manager has to change.

IBM's deep learning service, and the **FfDL** platform it became, is the through-line. A user
supplies code, a run command, a data location and a learner count; the platform containerizes
the framework image, preserves whatever internal communication that framework already uses,
and takes on everything else. Reliability comes from a per-job delegate created as a single
atomic operation, which rolls back and redeploys if it dies mid-provisioning, plus replicated
consensus storage for job status and object storage for checkpoints. The measured cost of all
this is about 5% against non-containerized bare metal, and up to 15% against specialized
hardware costing two to three times more — an economic argument, not a performance one.

Scheduling is where generic cluster managers fail deep learning most visibly, and the failures
are specific. Default spread placement fragments GPU clusters; per-pod scheduling temporarily
deadlocks distributed jobs, whose learners each seize a GPU and wait for siblings that will
never be scheduled. Replacing spread with packing, replayed against 60 days of arrivals from a
400-GPU production cluster, cut jobs queued longer than 15 minutes by more than 3×. Adding
gang scheduling drove idle GPUs — which reached 46% in the deadlocking case — and temporary
deadlocks to zero across every run. A scale test on roughly 680 GPUs sustained 700 concurrent
jobs at about 54,000 images processed per second; 12 of the 700 got stuck, every one traced to
a node with failed hardware. Major portions were released as open source.

**Effective elastic scaling** takes the next step and treats a training hyperparameter as a
schedulable resource. Existing schedulers move GPUs between jobs but never touch the job
itself; this work exploits the fact that a model's final accuracy survives a wide range of
batch sizes — measured at within ±0.5% across an eightfold range — to scale GPUs and batch size
together, choosing the allocation by dynamic programming in milliseconds. Against a baseline
that scales GPUs but fixes the batch, it completed up to twice as many jobs, dropped roughly
three times fewer, and improved average completion time by about 10×. It reports the honest
null result too: for jobs that cannot vary their batch size, the benefit is exactly zero.

A separate strand asked what GPUs are worth for classical analytics rather than deep learning.
That work kept the frameworks entirely stock — same APIs, same schedulers, same fault-tolerance
guarantees — and confined GPU code to user-level map and reduce functions, reaching up to 25×
on Spark and 18× on an in-memory MapReduce runtime over 100GB datasets. It also reports where
the gains stop: speedup flattens between 12 and 15 machines as communication and shuffle come
to dominate compute.

{% include theme_items.html theme=t_dl %}

## Cloud elasticity, trust, and compliance
<span class="theme-span">{{ t_cloud.span }}</span>

Before the machine learning work, a decade went into a different question: how do you make
cloud infrastructure behave predictably when you can neither see inside the application nor
trust the provider underneath it?

The first is **elasticity driven by application semantics rather than external metrics**. The
argument rests on a counterexample that recurs across the papers: a key-value store suffering
hot-key lock contention shows high CPU utilization, so a CPU-driven autoscaler adds nodes and
makes it worse. **ElasticRMI** made elasticity a property of a class — an elastic object pool
that clients address as a single remote object — and let the application supply the scaling
logic, provisioning in under 30 seconds where VM-level autoscaling took minutes. A control
experiment carried the real weight: the same system restricted to CPU and memory signals
performed like a conventional autoscaler, isolating the application metrics as what mattered.

That approach worked but demanded rewriting applications with deep knowledge of their
internals, so the next step inverted the burden. **Direct causality analysis** defines one
message as having caused another only if a control or data flow path connects them inside the
receiving component, and recovers those paths by static slicing, instrumenting only the
minimal set of variables whose provenance must be tracked. That requires recompilation and
nothing else — no annotations, no code changes — and the recovered path frequencies drive
proportional rather than uniform scaling. Two results make the point better than the headline:
full-fidelity tracing costs 27–38% runtime overhead and *worsens* provisioning, because the
tracing itself forces extra capacity; and sampling less is not monotonically better — 5%
sampling is lighter than 10% but up to 80% worse, because it fails to characterize the
workload. The sweet spot is empirical, around 10%.

**Concerto** applies the same instinct one layer down, in storage: a distributed in-memory
graph store whose distinguishing abstraction is the *view*, a named subgraph on which
applications register event handlers that the store runs server-side. On a road-network
application, reacting where the data lives beat client-side polling by up to two orders of
magnitude — the same bargain elasticity makes, one layer down.

The second strand is **trust and compliance**. Enterprises could not verify what software stack
a provider was running, nor that data stayed inside a jurisdiction. A trusted, geo-fenced
hybrid cloud architecture attested the boot chain and delegated per-package integrity to
signature appraisal, replacing a whitelist that had grown past 30GB in months with something
that scales linearly. That substrate was reused directly beneath a compliant analytics
platform, which turned regulatory requirements into selectable, re-testable modules — and
reported the price honestly: 25–40% end-to-end overhead for full security, dominated by wire
encryption. **INCOGNITO** attacked the same problem from the data side, anonymizing at scale
with distribution-aware bucketing that outperformed two established privacy models by 75% and
35% at 100GB.

The third strand is **measurement**. Every metric for intrusion detection accuracy assumed
fixed resources, which is wrong the moment a hypervisor can hotplug CPUs mid-operation.
Redrawing the system under test to include the hypervisor produced a metric that captures
this, along with a counterintuitive finding: underprovisioning can *earn* a reward, because
packets an overloaded detector never inspects are packets it never mislabels.

The earliest work here, at Purdue, asked whether model-based testing finds security bugs in
cryptographic protocol implementations. Published as a negative result, the answer was largely
no: statechart-derived tests reached only 51–81% MC/DC coverage of a TLS implementation, errors
injected into the uncovered code produced session hijack and authentication failure, and 70
hand-written negative tests added no coverage at all.

{% include theme_items.html theme=t_cloud %}

## Event correlation, publish/subscribe, and distributed programming
<span class="theme-span">{{ t_events.span }}</span>

The earliest body of work, and the one everything after it inherits from. The recurring bet is
that a compiler knows things a middleware cannot, and that making distributed behavior
explicit in the language is what lets the runtime be fast.

**EventJava** extends Java with event correlation as a first-class construct: event methods
declare event types implicitly, correlation patterns compose them, and guards separate *which*
events combine from *how* they are handled. The language was then deepened for four years, each
step a self-critique of the last. **GenTrie** replaced its Rete-based matcher with a
trie-based algorithm reaching 2.5× the throughput of a well-known Rete implementation and 10×
that of two concurrent-language alternatives. **Conspects** replaced its context mechanism,
making notions of time and space — physical clocks, Lamport clocks, vector clocks, geographic
coordinates — modular aspects that can be swapped without touching application logic. That
portability is measurable in both directions: the choice of clock representation swings
throughput by up to 40× on a tornado-monitoring workload, and the identical program runs
unchanged on x86 Linux and on a hard-real-time embedded board with only the aspect exchanged.

A companion paper turned the language's explicitness into compiler optimizations. Because
event types and guards are visible statically, the compiler can prove attributes are never
mutated and skip expensive cloning; convert guards into parametric subscriptions with virtual
boolean variables instead of re-subscription, worth up to 31% throughput and 3.5× fewer
spurious events; and infer causal dependencies to build independent multicast groups
automatically rather than funneling everything through one.

The second strand asks what can actually be *guaranteed* when correlation is decentralized and
processes crash — a problem as hard as consensus. **FAIDECS** builds an overlay of replicated
merger nodes that deterministically merge event flows, sustaining roughly 31,400 events per
second where total-order-broadcast alternatives managed about 3% of that. Its more durable
contribution is a vocabulary: named, formally stated delivery properties for composite events
where none existed, including covering agreement and three mutually independent orderings. A
later journal article turned that vocabulary into a compatibility matrix over matching and
disposal semantics, mapping four established correlation languages onto it so practitioners
could read off which guarantees survive — and proving the sharp negative results, notably that
one common matching rule cannot be made safe under *any* disposal semantics, and that sliding
windows are irreconcilable with no-duplication and need a weakened form of it.

The third strand is matching itself. **Parametric subscriptions** — awarded best paper at
Middleware 2010 — let a subscription's thresholds change as variable updates rather than
unsubscribe/subscribe pairs, which had been losing events during transitions and burning broker
CPU on bookkeeping; the journal version adds a monitor that spline-fits pathological update
rates and safely over-approximates. **Beretta** then closed the remaining gap: by normalizing
every subscription to carry exactly one condition per attribute, structural changes collapse
into bound updates too, and matching drops from linear to logarithmic in the number of
subscriptions. **FX-TM** generalized the machinery from boolean to scored partial matching for
ad exchanges, supporting negative weights, proration, and budget-driven score adjustment that
existing top-k algorithms could not express.

The habits formed here — decentralize the bottleneck, replicate the merge point, state the
guarantee formally, then measure against the centralized baseline — are the ones the later
cloud, deep learning, and federated learning work runs on.

{% include theme_items.html theme=t_events %}
