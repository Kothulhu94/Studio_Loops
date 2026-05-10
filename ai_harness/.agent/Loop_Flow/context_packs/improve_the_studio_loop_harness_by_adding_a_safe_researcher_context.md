# Context Pack: improve_the_studio_loop_harness_by_adding_a_safe / researcher

## Feature Goal
Improve the Studio Loop harness by adding a safer local-codebase audit path for researcher stages and reducing prompt bloat. Keep changes small and verify with tests.

## Current Stage
researcher

## Decision Memory
Refer to .agent/Loop_Flow/context_packs/improve_the_studio_loop_harness_by_adding_a_safe_decision_memory.md for stable decisions and constraints.

## Relevant Artifacts
{}

## Relevant Research Briefs
### Perform a technical audit of the Studio Loop harness, specifically focusing on the orchestration engine, existing ArtifactValidator implementation, and current blueprint/planning workflows to identify gaps in validation.
- Status: complete
- Artifact: improve_the_studio_loop_harness_by_adding_a_safe_researcher_Perform_a_technical_audit_of_t_research_brief.md
- Key Findings:
  - Found .agent/orchestrator/artifact_validator.py with class ArtifactValidator, def __init__, def validate_research_result, def validate, def _resolve_existing_artifact, def _find_satisfying_artifact (2
  - Found .agent/orchestrator/studio_loop.py with class StudioLoopOrchestrator, def __init__, def load_config, def run, def autonomous_loop, def acquire_lock (1018 lines).
  - Found .agent/orchestrator/research_client.py with def normalize_ascii_text, class ResearchClient, def __init__, def perform_research, def _perform_local_audit, def _perform_local_discovery (526 lines)



## Validation Status
[]

## Pruned Source Context
--- Context Pruning Map for: ['improve', 'studio', 'loop', 'harness', 'adding', 'safer', 'local-codebase', 'audit', 'path', 'researcher', 'stages', 'improve_the_studio_loop_harness_by_adding_a_safe_researcher_perform_a_technical_audit_of_t_research_brief.md', 'perform', 'technical', 'specifically', 'complete'] ---
ai_harness_bundle.txt: L1802-L1821, L1870-L1889, L1710-L1729, L7-L26, L1686-L1705
bundle_harness.bat: L19-L38, L1-L19, L71-L90, L50-L69, L72-L91
HANDOFF_SCHEMA.json: L98-L117, L1-L19, L6-L25, L48-L67, L50-L69
package-lock.json: L471-L490, L1211-L1230, L487-L506, L930-L949, L3-L22
package.json: L1-L14
README.md: L1-L17, L26-L33, L1-L15, L3-L22, L20-L33
.agent/bin/licenses/cloud.google.com/go/compute/metadata/LICENSE: L66-L85
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/.gitignore: L20-L39
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither.go: L363-L382
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/LICENSE: L266-L285, L91-L110, L311-L330
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/parallel.go: L27-L46
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/README.md: L102-L121, L1-L20
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/.github/workflows/test.yml: L4-L23, L1-L19
.agent/bin/licenses/github.com/minio/selfupdate/LICENSE: L66-L85
.agent/bin/licenses/github.com/spf13/afero/LICENSE.txt: L65-L84
.agent/bin/licenses/github.com/spf13/cobra/LICENSE.txt: L65-L84
.agent/bin/licenses/github.com/TheZoraiz/ascii-image-converter/LICENSE.txt: L66-L85
.agent/Loop_Flow/.gitkeep: Full File
.agent/Loop_Flow/autonomous_loop_refinement_blueprint.md: L5-L15, L1-L15, L3-L15
.agent/Loop_Flow/source_index.json: L583-L602, L553-L572, L463-L482, L657-L676, L523-L542
.agent/orchestrator/actions_schema.json: L60-L79, L35-L54, L7-L26, L63-L82, L18-L37
.agent/orchestrator/artifact_store.py: L11-L30, L15-L32, L20-L32, L18-L32, L7-L26
.agent/orchestrator/artifact_validator.py: L187-L206, L195-L214, L198-L217, L98-L117, L111-L130
.agent/orchestrator/browser_research.py: L211-L230, L339-L358, L314-L333, L328-L347, L338-L357
.agent/orchestrator/capability_registry.py: L167-L173, L41-L60, L105-L124, L165-L173, L100-L119
.agent/orchestrator/command_runner.py: L9-L28, L100-L107, L13-L32, L7-L26, L5-L24
.agent/orchestrator/config.json: L26-L45, L19-L38, L20-L39, L15-L34, L47-L66
.agent/orchestrator/context_compactor.py: L72-L91, L37-L56, L22-L41, L46-L65, L3-L22
.agent/orchestrator/context_pruner.py: L114-L133, L72-L91, L19-L38, L3-L22, L1-L20
.agent/orchestrator/copyright_guard.py: L9-L28, L3-L22, L1-L20, L7-L26, L2-L21
.agent/orchestrator/file_writer.py: L26-L45, L25-L44, L60-L79, L13-L32, L28-L47
.agent/orchestrator/graph.py: L11-L30, L36-L42, L37-L42, L1-L20, L13-L32
.agent/orchestrator/hooks.py: L3-L22, L21-L37
.agent/orchestrator/kobold_client.py: L17-L36, L71-L77, L16-L35, L14-L33, L69-L77
.agent/orchestrator/page_extractor.py: L21-L40, L23-L42, L25-L44, L88-L97, L80-L97
.agent/orchestrator/patch_applier.py: L11-L30, L26-L45, L100-L109, L28-L47, L7-L26
.agent/orchestrator/playwright_research.py: L17-L36, L9-L28, L7-L26, L15-L34, L16-L35
.agent/orchestrator/prompt_compiler.py: L41-L60, L46-L65, L35-L54, L3-L22, L43-L62
.agent/orchestrator/research_client.py: L327-L346, L223-L242, L293-L312, L131-L150, L98-L117
.agent/orchestrator/response_parser.py: L344-L363, L348-L367, L284-L303, L249-L268, L19-L38
.agent/orchestrator/retry_engine.py: L64-L83, L67-L86, L22-L41, L45-L64, L68-L87
.agent/orchestrator/role_loader.py: L22-L41, L56-L73, L23-L42, L31-L50, L35-L54
.agent/orchestrator/safety_guard.py: L92-L111, L7-L26, L117-L136, L67-L86, L71-L90
.agent/orchestrator/search_result_parser.py: L108-L127, L44-L63, L65-L84, L43-L62, L80-L99
.agent/orchestrator/session_router.py: L11-L30, L25-L44, L28-L47, L7-L26, L119-L135
.agent/orchestrator/skill_registry.py: L26-L45, L44-L63, L95-L113, L25-L44, L92-L111
.agent/orchestrator/source_indexer.py: L62-L79, L70-L79, L37-L56, L44-L63, L23-L42
.agent/orchestrator/state_store.py: L108-L127, L124-L143, L131-L150, L111-L130, L130-L149
.agent/orchestrator/studio_loop.py: L122-L141, L147-L166, L566-L585, L383-L402, L866-L885
.agent/orchestrator/transition_engine.py: L21-L40, L30-L49, L64-L69, L55-L69, L28-L47
.agent/orchestrator/templates/stage_prompt.md: L36-L55, L37-L56, L1-L15, L9-L28, L10-L29
.agent/orchestrator/__pycache__/artifact_store.cpython-312.pyc: L2-L21, L21-L28, L1-L18
.agent/orchestrator/__pycache__/artifact_store.cpython-314.pyc: L1-L17, L16-L29, L1-L19
.agent/orchestrator/__pycache__/artifact_validator.cpython-312.pyc: L36-L55, L1-L17, L86-L95, L38-L57, L3-L22
.agent/orchestrator/__pycache__/artifact_validator.cpython-314.pyc: L108-L127, L45-L64, L44-L63, L41-L60, L4-L23
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc: L84-L103, L120-L139, L119-L138, L13-L32, L117-L136
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc.2709833153488: L56-L75, L84-L103, L45-L64, L41-L60, L43-L62
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc: L124-L143, L131-L150, L22-L41, L123-L142, L35-L54
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc.3073430176800: L64-L83, L9-L28, L29-L48, L31-L50, L60-L79
.agent/orchestrator/__pycache__/capability_registry.cpython-312.pyc: L31-L50, L10-L29, L12-L31
.agent/orchestrator/__pycache__/capability_registry.cpython-314.pyc: L44-L63, L10-L29
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-312.pyc: L1-L17, L12-L31, L48-L60
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-314.pyc: L6-L25, L39-L49, L1-L18
.agent/orchestrator/__pycache__/command_runner.cpython-312.pyc: L51-L63, L1-L20
.agent/orchestrator/__pycache__/command_runner.cpython-314.pyc: L52-L68, L16-L35, L1-L20
.agent/orchestrator/__pycache__/context_compactor.cpython-312.pyc: L48-L67, L3-L22, L1-L18, L1-L19
.agent/orchestrator/__pycache__/context_compactor.cpython-314.pyc: L49-L68, L3-L22, L1-L18, L1-L19
.agent/orchestrator/__pycache__/context_pruner.cpython-312.pyc: L21-L40, L35-L54, L10-L29, L34-L53, L1-L18
.agent/orchestrator/__pycache__/context_pruner.cpython-314.pyc: L25-L44, L1-L16, L15-L34, L39-L58, L59-L78
.agent/orchestrator/__pycache__/copyright_guard.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/copyright_guard.cpython-314.pyc: L1-L20
.agent/orchestrator/__pycache__/file_writer.cpython-312.pyc: L17-L36, L30-L49, L29-L48, L1-L20, L15-L34
.agent/orchestrator/__pycache__/file_writer.cpython-314.pyc: L17-L36, L29-L48, L31-L50, L1-L20, L28-L47
.agent/orchestrator/__pycache__/graph.cpython-312.pyc: L11-L23, L15-L23, L14-L23, L13-L23, L1-L20
.agent/orchestrator/__pycache__/graph.cpython-314.pyc: L11-L30, L23-L37, L9-L28, L10-L29, L21-L37
.agent/orchestrator/__pycache__/hooks.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/hooks.cpython-314.pyc: L1-L16
.agent/orchestrator/__pycache__/kobold_client.cpython-312.pyc: L1-L17, L1-L19
.agent/orchestrator/__pycache__/kobold_client.cpython-314.pyc: L2-L21, L1-L20, L1-L18
.agent/orchestrator/__pycache__/page_extractor.cpython-312.pyc: L36-L55, L2-L21, L34-L53, L1-L20
.agent/orchestrator/__pycache__/page_extractor.cpython-314.pyc: L32-L51, L34-L53, L1-L19
.agent/orchestrator/__pycache__/patch_applier.cpython-312.pyc: L1-L17, L26-L45, L55-L60, L22-L41, L28-L47
.agent/orchestrator/__pycache__/patch_applier.cpython-314.pyc: L22-L41, L63-L68, L1-L20, L4-L23, L1-L16
.agent/orchestrator/__pycache__/playwright_research.cpython-312.pyc: L14-L33, L1-L18, L1-L19
.agent/orchestrator/__pycache__/playwright_research.cpython-314.pyc: L14-L33, L1-L20, L1-L19
.agent/orchestrator/__pycache__/prompt_compiler.cpython-312.pyc: L17-L36, L11-L30, L1-L19, L10-L29, L1-L18
.agent/orchestrator/__pycache__/prompt_compiler.cpython-314.pyc: L1-L17, L11-L30, L26-L45, L25-L44, L29-L48
.agent/orchestrator/__pycache__/research_client.cpython-312.pyc: L45-L64, L13-L32, L66-L82, L5-L24, L16-L35
.agent/orchestrator/__pycache__/research_client.cpython-314.pyc: L19-L38, L44-L63, L190-L209, L145-L164, L101-L120
.agent/orchestrator/__pycache__/response_parser.cpython-312.pyc: L1-L17, L16-L35
.agent/orchestrator/__pycache__/response_parser.cpython-314.pyc: L96-L115, L98-L117, L93-L112, L1-L16, L18-L37
.agent/orchestrator/__pycache__/retry_engine.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/retry_engine.cpython-314.pyc: L114-L133, L72-L91, L70-L89, L102-L121, L1-L16
.agent/orchestrator/__pycache__/role_loader.cpython-312.pyc: L9-L28, L3-L22, L4-L23, L6-L25, L8-L27
.agent/orchestrator/__pycache__/role_loader.cpython-314.pyc: L7-L26, L6-L25, L4-L23
.agent/orchestrator/__pycache__/safety_guard.cpython-312.pyc: L22-L41, L29-L48, L39-L55, L28-L47, L4-L23
.agent/orchestrator/__pycache__/safety_guard.cpython-314.pyc: L26-L45, L19-L38, L21-L40, L20-L39, L4-L23
.agent/orchestrator/__pycache__/search_result_parser.cpython-312.pyc: L1-L17, L19-L38
.agent/orchestrator/__pycache__/search_result_parser.cpython-314.pyc: L1-L16, L22-L41
.agent/orchestrator/__pycache__/session_router.cpython-312.pyc: L36-L55, L30-L49, L29-L48, L10-L29, L31-L50
.agent/orchestrator/__pycache__/session_router.cpython-314.pyc: L22-L41, L111-L126, L23-L42, L20-L39, L3-L22
.agent/orchestrator/__pycache__/skill_registry.cpython-312.pyc: L36-L55, L22-L41, L7-L26, L54-L61, L6-L25
.agent/orchestrator/__pycache__/skill_registry.cpython-314.pyc: L36-L55, L42-L58, L23-L42, L20-L39, L10-L29
.agent/orchestrator/__pycache__/source_indexer.cpython-312.pyc: L23-L42, L10-L29, L1-L20, L1-L18, L1-L19
.agent/orchestrator/__pycache__/source_indexer.cpython-314.pyc: L1-L17, L20-L39, L10-L29, L1-L18, L1-L19
.agent/orchestrator/__pycache__/source_summarizer.cpython-312.pyc: L1-L7
.agent/orchestrator/__pycache__/state_store.cpython-312.pyc: L36-L55, L108-L127, L96-L115, L116-L135, L9-L28
.agent/orchestrator/__pycache__/state_store.cpython-314.pyc: L112-L131, L30-L49, L29-L48, L109-L128, L4-L23
.agent/orchestrator/__pycache__/studio_loop.cpython-312.pyc: L26-L45, L22-L41, L19-L38, L111-L130, L143-L162
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc: L327-L346, L26-L45, L211-L230, L93-L112, L334-L353
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc.3098252610704: L26-L45, L173-L192, L22-L41, L19-L38, L130-L149
.agent/orchestrator/__pycache__/test_runner.cpython-312.pyc: L1-L18
.agent/orchestrator/__pycache__/test_runner.cpython-314.pyc: L1-L18
.agent/orchestrator/__pycache__/transition_engine.cpython-312.pyc: L7-L26, L1-L17, L13-L32
.agent/orchestrator/__pycache__/transition_engine.cpython-314.pyc: L1-L16, L2-L21, L10-L29
.agent/orchestrator/__pycache__/web_fetcher.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/web_research.cpython-312.pyc: L1-L17
.agent/skills/asset_creator_skills.md: L33-L43
.agent/skills/designer_skills.md: L51-L60, L22-L41, L25-L44, L15-L34, L49-L60
.agent/skills/developer_skills.md: L58-L63, L52-L63, L48-L63, L57-L63, L51-L63
.agent/skills/producer_skills.md: L9-L28, L27-L46, L41-L48
.agent/skills/qa_skills.md: L39-L48, L17-L36, L26-L45, L22-L41, L21-L40
.agent/skills/registry.json: L5-L13, L4-L13, L1-L13, L2-L13, L3-L13
.agent/skills/researcher_skills.md: L87-L97, L1-L15, L10-L29, L35-L54, L1-L20
.agent/skills/asset_creator/skill.json: L1-L15, L2-L15, L4-L15
.agent/skills/asset_creator/SKILL.md: L1-L3
.agent/skills/bug_hunter/skill.json: L1-L16, L1-L17, L2-L20, L6-L20
.agent/skills/bug_hunter/SKILL.md: L1-L3
.agent/skills/debug_dev/skill.json: L1-L15, L2-L15, L4-L15
.agent/skills/debug_dev/SKILL.md: L1-L3
.agent/skills/designer/skill.json: L1-L16, L1-L17, L2-L20, L6-L20
.agent/skills/designer/SKILL.md: L1-L3
.agent/skills/developer/skill.json: L1-L15, L2-L15, L4-L15
.agent/skills/developer/SKILL.md: L1-L3
.agent/skills/producer/skill.json: L1-L16, L1-L17, L2-L20, L6-L20
.agent/skills/producer/SKILL.md: L1-L3
.agent/skills/qa/skill.json: L1-L16, L1-L17, L2-L20, L6-L20
.agent/skills/qa/SKILL.md: L1-L3
.agent/skills/researcher/skill.json: L1-L17, L10-L21, L8-L21, L1-L16, L2-L21
.agent/skills/researcher/SKILL.md: L1-L3
.agent/workflows/asset_creator.md: L25-L42, L19-L38, L35-L42, L3-L22, L16-L35
.agent/workflows/bug_hunter.md: L21-L40, L17-L36, L33-L40, L4-L23
.agent/workflows/concept_producer.md: L32-L51, L33-L51, L44-L51, L4-L23
.agent/workflows/debug_dev.md: L34-L41, L4-L23
.agent/workflows/designer.md: L17-L36, L36-L43, L23-L42, L3-L22, L24-L43
.agent/workflows/developer.md: L56-L63, L20-L39, L10-L29, L3-L22, L49-L63
.agent/workflows/qa_tester.md: L21-L40, L20-L39, L3-L22, L60-L67, L40-L59
.agent/workflows/researcher.md: L48-L61, L25-L44, L10-L29, L3-L22, L13-L32
.agent/workflows/STUDIO_LOOP_WORKFLOW.md: L1-L18, L23-L42, L30-L49, L1-L20, L27-L46
.agent/workflows/task_template.md: L22-L41, L21-L40, L30-L49, L10-L29, L13-L32
docs/local_setup.md: L36-L55, L58-L63, L1-L17, L10-L29, L50-L63
docs/verification/browser_research_mdn_requestanimationframe.md: L22-L41, L25-L44, L31-L50, L28-L47, L37-L53
tests/e2e_loop_test.py: L122-L141, L124-L143, L11-L30, L22-L41, L19-L38
tests/real_browser_research_check.py: L37-L56, L1-L19, L41-L60, L3-L22, L35-L54
tests/regression_page_extractor.py: L1-L18
tests/test_autonomous_loop.py: L19-L38, L44-L63, L25-L44, L28-L47, L7-L26
tests/test_browser_research_mock.py: L105-L124, L119-L138, L13-L32, L55-L74, L95-L114
tests/test_gemma4_factory_tuning.py: L35-L51, L1-L20
tests/test_kobold_client.py: L23-L42, L11-L30, L4-L23
tests/test_local_codebase_audit.py: L108-L127, L147-L166, L327-L346, L435-L454, L441-L460
tests/test_repair_prompt.py: L98-L117, L190-L209, L13-L32, L145-L164, L7-L26
tests/test_response_parser.py: L108-L127, L340-L359, L230-L249, L173-L192, L383-L402
tests/test_robustness.py: L91-L105, L28-L47, L13-L32, L6-L25, L48-L67
tests/test_sessions_and_skills.py: L173-L192, L131-L150, L22-L41, L212-L231, L98-L117
tests/fixtures/research_mdn_requestanimationframe.json: L1-L16, L15-L24
tests/__pycache__/test_browser_research_mock.cpython-314.pyc: L104-L123, L23-L42, L25-L44, L29-L48, L5-L24
tests/__pycache__/test_repair_prompt.cpython-314.pyc: L108-L127, L147-L166, L22-L41, L145-L164, L55-L74
tests/__pycache__/test_response_parser.cpython-314.pyc: L36-L55, L78-L97, L11-L30, L96-L115, L23-L42
tests/__pycache__/test_robustness.cpython-314.pyc: L10-L29, L3-L22, L62-L81, L61-L80, L14-L33
tools/bootstrap_local_env.py: L78-L97, L48-L67, L47-L66, L97-L116
tools/bundle_project.py: L48-L67, L67-L86, L75-L94, L50-L69, L57-L76
tools/check_perms.py: L7-L25, L12-L25, L3-L22, L1-L20, L2-L21
tools/context_culler.py: L11-L30, L26-L45, L13-L32, L99-L104, L50-L69
tools/find_bloat.py: L17-L36, L1-L17, L19-L38, L23-L42, L1-L20
tools/test_orchestrator.py: L105-L124, L93-L112, L92-L111, L7-L26, L55-L74
tools/verify_clean_runtime.py: L108-L127, L124-L143, L230-L249, L198-L217, L212-L231
tools/__pycache__/verify_clean_runtime.cpython-314.pyc: L76-L89, L37-L56, L19-L38, L20-L39, L10-L29
tools/__pycache__/__init__.cpython-314.pyc: L1-L2

