# Context Pack: improve_the_studio_loop_harness_by_adding_a_safe / qa_tester

## Feature Goal
Improve the Studio Loop harness by adding a safer local-codebase audit path for researcher stages and reducing prompt bloat. Keep changes small and verify with tests.

## Current Stage
qa_tester

## Decision Memory
Refer to .agent/Loop_Flow/context_packs/improve_the_studio_loop_harness_by_adding_a_safe_decision_memory.md for stable decisions and constraints.

## Relevant Artifacts
{
  "improve_the_studio_loop_harness_by_adding_a_safe_blueprint.md": ".agent/Loop_Flow/improve_the_studio_loop_harness_by_adding_a_safe_blueprint.md"
}

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
--- Context Pruning Map for: ['improve', 'studio', 'loop', 'harness', 'adding', 'safer', 'local-codebase', 'audit', 'path', 'researcher', 'stages', 'qa_tester', 'improve_the_studio_loop_harness_by_adding_a_safe_researcher_perform_a_technical_audit_of_t_research_brief.md', 'perform', 'technical', 'specifically', 'complete'] ---
ai_harness_bundle.txt: L34-L53, L1802-L1821, L1935-L1954, L1820-L1839, L54-L73
bundle_harness.bat: L19-L38, L46-L65, L72-L91, L54-L73, L71-L90
HANDOFF_SCHEMA.json: L17-L36, L34-L53, L46-L65, L1-L20, L72-L91
package-lock.json: L487-L506, L930-L949, L928-L947, L471-L490, L1-L16
package.json: L1-L14
README.md: L26-L33, L1-L17, L20-L33, L3-L22, L12-L31
.agent/bin/licenses/cloud.google.com/go/compute/metadata/LICENSE: L66-L85
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/.gitignore: L20-L39
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither.go: L363-L382
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/LICENSE: L311-L330, L266-L285, L91-L110
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/parallel.go: L27-L46
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/README.md: L102-L121, L1-L20
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/.github/workflows/test.yml: L4-L23, L1-L19
.agent/bin/licenses/github.com/minio/selfupdate/LICENSE: L66-L85
.agent/bin/licenses/github.com/spf13/afero/LICENSE.txt: L65-L84
.agent/bin/licenses/github.com/spf13/cobra/LICENSE.txt: L65-L84
.agent/bin/licenses/github.com/TheZoraiz/ascii-image-converter/LICENSE.txt: L66-L85
.agent/Loop_Flow/.gitkeep: Full File
.agent/Loop_Flow/autonomous_loop_refinement_blueprint.md: L5-L15, L1-L15, L3-L15
.agent/Loop_Flow/context_map.json: Full File
.agent/Loop_Flow/improve_the_studio_loop_harness_by_adding_a_safe_blueprint.md: L1-L18, L38-L43, L11-L30, L15-L34, L3-L22
.agent/Loop_Flow/source_index.json: L735-L754, L765-L784, L154-L173, L511-L530, L571-L590
.agent/orchestrator/actions_schema.json: L47-L66, L35-L54, L18-L37, L7-L26, L11-L30
.agent/orchestrator/artifact_store.py: L25-L32, L18-L32, L19-L32, L11-L30, L7-L26
.agent/orchestrator/artifact_validator.py: L34-L53, L226-L234, L228-L234, L111-L130, L1-L20
.agent/orchestrator/browser_research.py: L342-L361, L64-L83, L211-L230, L314-L333, L355-L364
.agent/orchestrator/capability_registry.py: L166-L173, L167-L173, L165-L173, L100-L119, L41-L60
.agent/orchestrator/command_runner.py: L69-L88, L100-L107, L13-L32, L18-L37, L7-L26
.agent/orchestrator/config.json: L19-L38, L47-L66, L20-L39, L15-L34, L26-L45
.agent/orchestrator/context_compactor.py: L46-L65, L53-L72, L72-L91, L86-L92, L56-L75
.agent/orchestrator/context_pruner.py: L19-L38, L1-L18, L59-L78, L53-L72, L1-L20
.agent/orchestrator/copyright_guard.py: L1-L20, L65-L72, L2-L21, L7-L26, L9-L28
.agent/orchestrator/file_writer.py: L34-L53, L93-L102, L46-L65, L84-L102, L92-L102
.agent/orchestrator/graph.py: L1-L18, L1-L20, L36-L42, L31-L42, L13-L32
.agent/orchestrator/hooks.py: L21-L37, L3-L22
.agent/orchestrator/kobold_client.py: L17-L36, L66-L77, L71-L77, L69-L77, L16-L35
.agent/orchestrator/page_extractor.py: L74-L93, L24-L43, L80-L97, L25-L44, L88-L97
.agent/orchestrator/patch_applier.py: L69-L88, L52-L71, L11-L30, L7-L26, L9-L28
.agent/orchestrator/playwright_research.py: L17-L36, L53-L72, L7-L26, L15-L34, L9-L28
.agent/orchestrator/prompt_compiler.py: L46-L65, L43-L62, L48-L67, L69-L88, L35-L54
.agent/orchestrator/research_client.py: L34-L53, L251-L270, L293-L312, L71-L90, L64-L83
.agent/orchestrator/response_parser.py: L347-L366, L19-L38, L352-L371, L20-L39, L351-L370
.agent/orchestrator/retry_engine.py: L68-L87, L24-L43, L35-L54, L80-L99, L20-L39
.agent/orchestrator/role_loader.py: L31-L50, L55-L73, L24-L43, L35-L54, L32-L51
.agent/orchestrator/safety_guard.py: L69-L88, L52-L71, L72-L91, L117-L136, L7-L26
.agent/orchestrator/search_result_parser.py: L43-L62, L108-L127, L80-L99, L65-L84, L44-L63
.agent/orchestrator/session_router.py: L17-L36, L19-L38, L20-L39, L11-L30, L7-L26
.agent/orchestrator/skill_registry.py: L17-L36, L30-L49, L61-L80, L71-L90, L65-L84
.agent/orchestrator/source_indexer.py: L34-L53, L53-L72, L24-L43, L35-L54, L37-L56
.agent/orchestrator/state_store.py: L111-L130, L129-L148, L167-L186, L27-L46, L4-L23
.agent/orchestrator/studio_loop.py: L719-L738, L745-L764, L46-L65, L495-L514, L735-L754
.agent/orchestrator/transition_engine.py: L49-L68, L64-L69, L62-L69, L46-L65, L55-L69
.agent/orchestrator/templates/stage_prompt.md: L36-L55, L8-L27, L35-L54, L37-L56, L80-L99
.agent/orchestrator/__pycache__/artifact_store.cpython-312.pyc: L1-L18, L2-L21, L21-L28
.agent/orchestrator/__pycache__/artifact_store.cpython-314.pyc: L16-L29, L1-L17, L1-L19
.agent/orchestrator/__pycache__/artifact_validator.cpython-312.pyc: L36-L55, L1-L17, L38-L57, L2-L21, L40-L59
.agent/orchestrator/__pycache__/artifact_validator.cpython-314.pyc: L1-L18, L46-L65, L108-L127, L8-L27, L91-L110
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc: L119-L138, L117-L136, L120-L139, L13-L32, L91-L110
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc.2709833153488: L49-L68, L46-L65, L43-L62, L87-L106, L56-L75
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc: L131-L150, L35-L54, L155-L174, L125-L144, L124-L143
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc.3073430176800: L31-L50, L32-L51, L29-L48, L9-L28, L61-L80
.agent/orchestrator/__pycache__/capability_registry.cpython-312.pyc: L12-L31, L31-L50, L10-L29
.agent/orchestrator/__pycache__/capability_registry.cpython-314.pyc: L44-L63, L10-L29
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-312.pyc: L12-L31, L48-L60, L1-L17
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-314.pyc: L1-L18, L39-L49, L6-L25
.agent/orchestrator/__pycache__/command_runner.cpython-312.pyc: L51-L63, L1-L20
.agent/orchestrator/__pycache__/command_runner.cpython-314.pyc: L16-L35, L52-L68, L1-L20
.agent/orchestrator/__pycache__/context_compactor.cpython-312.pyc: L1-L18, L3-L22, L48-L67, L1-L19
.agent/orchestrator/__pycache__/context_compactor.cpython-314.pyc: L49-L68, L1-L18, L3-L22, L1-L19
.agent/orchestrator/__pycache__/context_pruner.cpython-312.pyc: L34-L53, L1-L18, L35-L54, L21-L40, L65-L77
.agent/orchestrator/__pycache__/context_pruner.cpython-314.pyc: L59-L78, L25-L44, L1-L16, L15-L34, L39-L58
.agent/orchestrator/__pycache__/copyright_guard.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/copyright_guard.cpython-314.pyc: L1-L20
.agent/orchestrator/__pycache__/file_writer.cpython-312.pyc: L17-L36, L1-L20, L8-L27, L32-L51, L29-L48
.agent/orchestrator/__pycache__/file_writer.cpython-314.pyc: L17-L36, L31-L50, L1-L20, L2-L21, L18-L37
.agent/orchestrator/__pycache__/graph.cpython-312.pyc: L7-L23, L9-L23, L1-L20, L2-L21, L13-L23
.agent/orchestrator/__pycache__/graph.cpython-314.pyc: L24-L37, L1-L20, L21-L37, L13-L32, L11-L30
.agent/orchestrator/__pycache__/hooks.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/hooks.cpython-314.pyc: L1-L16
.agent/orchestrator/__pycache__/kobold_client.cpython-312.pyc: L1-L17, L1-L19
.agent/orchestrator/__pycache__/kobold_client.cpython-314.pyc: L1-L18, L2-L21, L1-L20
.agent/orchestrator/__pycache__/page_extractor.cpython-312.pyc: L34-L53, L36-L55, L2-L21, L1-L20
.agent/orchestrator/__pycache__/page_extractor.cpython-314.pyc: L34-L53, L32-L51, L1-L19
.agent/orchestrator/__pycache__/patch_applier.cpython-312.pyc: L1-L17, L55-L60, L7-L26, L46-L60, L22-L41
.agent/orchestrator/__pycache__/patch_applier.cpython-314.pyc: L48-L67, L1-L20, L24-L43, L2-L21, L18-L37
.agent/orchestrator/__pycache__/playwright_research.cpython-312.pyc: L1-L18, L14-L33, L1-L19
.agent/orchestrator/__pycache__/playwright_research.cpython-314.pyc: L1-L20, L14-L33, L1-L19
.agent/orchestrator/__pycache__/prompt_compiler.cpython-312.pyc: L17-L36, L1-L18, L11-L30, L1-L19, L14-L33
.agent/orchestrator/__pycache__/prompt_compiler.cpython-314.pyc: L31-L50, L1-L18, L34-L53, L1-L17, L24-L43
.agent/orchestrator/__pycache__/research_client.cpython-312.pyc: L66-L82, L13-L32, L45-L64, L1-L19, L5-L24
.agent/orchestrator/__pycache__/research_client.cpython-314.pyc: L19-L38, L20-L39, L9-L28, L71-L90, L145-L164
.agent/orchestrator/__pycache__/response_parser.cpython-312.pyc: L16-L35, L1-L17
.agent/orchestrator/__pycache__/response_parser.cpython-314.pyc: L94-L113, L96-L115, L18-L37, L1-L16, L95-L114
.agent/orchestrator/__pycache__/retry_engine.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/retry_engine.cpython-314.pyc: L74-L93, L101-L120, L72-L91, L103-L122, L102-L121
.agent/orchestrator/__pycache__/role_loader.cpython-312.pyc: L8-L27, L9-L28, L6-L25, L3-L22, L4-L23
.agent/orchestrator/__pycache__/role_loader.cpython-314.pyc: L7-L26, L4-L23, L6-L25
.agent/orchestrator/__pycache__/safety_guard.cpython-312.pyc: L24-L43, L25-L44, L29-L48, L6-L25, L22-L41
.agent/orchestrator/__pycache__/safety_guard.cpython-314.pyc: L19-L38, L20-L39, L21-L40, L38-L54, L22-L41
.agent/orchestrator/__pycache__/search_result_parser.cpython-312.pyc: L19-L38, L1-L17
.agent/orchestrator/__pycache__/search_result_parser.cpython-314.pyc: L1-L16, L22-L41
.agent/orchestrator/__pycache__/session_router.cpython-312.pyc: L31-L50, L36-L55, L118-L128, L8-L27, L29-L48
.agent/orchestrator/__pycache__/session_router.cpython-314.pyc: L24-L43, L20-L39, L2-L21, L29-L48, L113-L126
.agent/orchestrator/__pycache__/skill_registry.cpython-312.pyc: L54-L61, L36-L55, L24-L43, L7-L26, L6-L25
.agent/orchestrator/__pycache__/skill_registry.cpython-314.pyc: L36-L55, L20-L39, L2-L21, L42-L58, L23-L42
.agent/orchestrator/__pycache__/source_indexer.cpython-312.pyc: L1-L18, L1-L20, L8-L27, L23-L42, L1-L19
.agent/orchestrator/__pycache__/source_indexer.cpython-314.pyc: L1-L18, L1-L17, L8-L27, L20-L39, L1-L19
.agent/orchestrator/__pycache__/source_summarizer.cpython-312.pyc: L1-L7
.agent/orchestrator/__pycache__/state_store.cpython-312.pyc: L36-L55, L110-L129, L116-L135, L35-L54, L96-L115
.agent/orchestrator/__pycache__/state_store.cpython-314.pyc: L109-L128, L99-L118, L102-L121, L29-L48, L118-L137
.agent/orchestrator/__pycache__/studio_loop.cpython-312.pyc: L19-L38, L182-L201, L111-L130, L69-L88, L52-L71
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc: L46-L65, L286-L305, L294-L313, L72-L91, L275-L294
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc.3098252610704: L19-L38, L46-L65, L129-L148, L102-L121, L7-L26
.agent/orchestrator/__pycache__/test_runner.cpython-312.pyc: L1-L18
.agent/orchestrator/__pycache__/test_runner.cpython-314.pyc: L1-L18
.agent/orchestrator/__pycache__/transition_engine.cpython-312.pyc: L7-L26, L1-L17, L13-L32
.agent/orchestrator/__pycache__/transition_engine.cpython-314.pyc: L1-L16, L2-L21, L10-L29
.agent/orchestrator/__pycache__/web_fetcher.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/web_research.cpython-312.pyc: L1-L17
.agent/skills/asset_creator_skills.md: L33-L43
.agent/skills/designer_skills.md: L8-L27, L25-L44, L49-L60, L15-L34, L22-L41
.agent/skills/developer_skills.md: L58-L63, L51-L63, L52-L63, L57-L63, L48-L63
.agent/skills/producer_skills.md: L41-L48, L9-L28, L27-L46
.agent/skills/qa_skills.md: L17-L36, L37-L48, L39-L48, L21-L40, L22-L41
.agent/skills/registry.json: L1-L13, L3-L13, L4-L13, L6-L13, L5-L13
.agent/skills/researcher_skills.md: L1-L20, L52-L71, L35-L54, L1-L16, L58-L77
.agent/skills/asset_creator/skill.json: L1-L15, L2-L15, L4-L15
.agent/skills/asset_creator/SKILL.md: L1-L3
.agent/skills/bug_hunter/skill.json: L2-L20, L1-L16, L6-L20, L1-L17
.agent/skills/bug_hunter/SKILL.md: L1-L3
.agent/skills/debug_dev/skill.json: L1-L15, L2-L15, L4-L15
.agent/skills/debug_dev/SKILL.md: L1-L3
.agent/skills/designer/skill.json: L2-L20, L1-L16, L6-L20, L1-L17
.agent/skills/designer/SKILL.md: L1-L3
.agent/skills/developer/skill.json: L1-L15, L2-L15, L4-L15
.agent/skills/developer/SKILL.md: L1-L3
.agent/skills/producer/skill.json: L2-L20, L1-L16, L6-L20, L1-L17
.agent/skills/producer/SKILL.md: L1-L3
.agent/skills/qa/skill.json: L1-L17, L1-L16, L6-L20, L1-L19, L2-L20
.agent/skills/qa/SKILL.md: L1-L3
.agent/skills/researcher/skill.json: L13-L21, L1-L17, L6-L21, L8-L21, L2-L21
.agent/skills/researcher/SKILL.md: L1-L3
.agent/workflows/asset_creator.md: L19-L38, L25-L42, L35-L42, L3-L22, L16-L35
.agent/workflows/bug_hunter.md: L17-L36, L33-L40, L4-L23, L21-L40
.agent/workflows/concept_producer.md: L32-L51, L4-L23, L33-L51, L44-L51
.agent/workflows/debug_dev.md: L4-L23, L34-L41
.agent/workflows/designer.md: L17-L36, L36-L43, L24-L43, L23-L42, L3-L22
.agent/workflows/developer.md: L34-L53, L56-L63, L20-L39, L40-L59, L49-L63
.agent/workflows/qa_tester.md: L20-L39, L21-L40, L60-L67, L40-L59, L3-L22
.agent/workflows/researcher.md: L54-L61, L34-L53, L1-L18, L48-L61, L25-L44
.agent/workflows/STUDIO_LOOP_WORKFLOW.md: L17-L36, L1-L20, L78-L96, L21-L40, L30-L49
.agent/workflows/task_template.md: L1-L18, L13-L32, L21-L40, L47-L54, L15-L34
docs/local_setup.md: L58-L63, L36-L55, L1-L17, L2-L21, L50-L63
docs/verification/browser_research_mdn_requestanimationframe.md: L31-L50, L1-L18, L37-L53, L25-L44, L46-L53
tests/e2e_loop_test.py: L19-L38, L52-L71, L75-L94, L11-L30, L7-L26
tests/real_browser_research_check.py: L34-L53, L35-L54, L32-L51, L48-L65, L3-L22
tests/regression_page_extractor.py: L1-L18
tests/test_autonomous_loop.py: L17-L36, L19-L38, L72-L91, L7-L26, L93-L107
tests/test_browser_research_mock.py: L46-L65, L102-L121, L174-L190, L118-L137, L9-L28
tests/test_gemma4_factory_tuning.py: L35-L51, L1-L20
tests/test_kobold_client.py: L23-L42, L4-L23, L11-L30
tests/test_local_codebase_audit.py: L352-L371, L54-L73, L71-L90, L324-L343, L431-L450
tests/test_repair_prompt.py: L220-L239, L241-L260, L251-L270, L91-L110, L7-L26
tests/test_response_parser.py: L389-L408, L384-L403, L20-L39, L102-L121, L340-L359
tests/test_robustness.py: L34-L53, L46-L65, L52-L71, L72-L91, L21-L40
tests/test_sessions_and_skills.py: L111-L130, L133-L152, L142-L161, L141-L160, L125-L144
tests/fixtures/research_mdn_requestanimationframe.json: L1-L16, L15-L24
tests/__pycache__/test_browser_research_mock.cpython-314.pyc: L74-L93, L103-L122, L24-L43, L25-L44, L42-L61
tests/__pycache__/test_repair_prompt.cpython-314.pyc: L17-L36, L151-L170, L145-L164, L64-L83, L147-L166
tests/__pycache__/test_response_parser.cpython-314.pyc: L31-L50, L36-L55, L52-L71, L42-L61, L96-L115
tests/__pycache__/test_robustness.cpython-314.pyc: L65-L82, L61-L80, L3-L22, L62-L81, L14-L33
tools/bootstrap_local_env.py: L78-L97, L97-L116, L47-L66, L48-L67
tools/bundle_project.py: L34-L53, L52-L71, L75-L94, L54-L73, L61-L80
tools/check_perms.py: L1-L18, L1-L20, L2-L21, L12-L25, L3-L22
tools/context_culler.py: L17-L36, L34-L53, L11-L30, L9-L28, L30-L49
tools/find_bloat.py: L17-L36, L19-L38, L33-L45, L1-L17, L1-L20
tools/test_orchestrator.py: L17-L36, L20-L39, L102-L121, L7-L26, L76-L95
tools/verify_clean_runtime.py: L19-L38, L270-L289, L286-L305, L251-L270, L117-L136
tools/__pycache__/verify_clean_runtime.cpython-314.pyc: L19-L38, L59-L78, L20-L39, L62-L81, L74-L89
tools/__pycache__/__init__.cpython-314.pyc: L1-L2

