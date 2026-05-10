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
No research results available yet.

## Validation Status
[]

## Pruned Source Context
--- Context Pruning Map for: ['improve', 'studio', 'loop', 'harness', 'adding', 'safer', 'local-codebase', 'audit', 'path', 'researcher', 'stages'] ---
ai_harness_bundle.txt: L1724-L1743, L1783-L1802, L1681-L1700, L1677-L1696, L1856-L1875
bundle_harness.bat: L64-L83, L3-L22, L54-L73, L67-L83, L35-L54
HANDOFF_SCHEMA.json: L64-L83, L50-L69, L33-L52, L80-L99, L96-L115
package-lock.json: L3-L22, L471-L490, L928-L947, L1-L16, L487-L506
package.json: L1-L14
README.md: L12-L31, L3-L22, L1-L17, L20-L33, L1-L15
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither.go: L363-L382
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/parallel.go: L27-L46
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/.github/workflows/test.yml: L1-L19, L4-L23
.agent/Loop_Flow/.gitkeep: Full File
.agent/Loop_Flow/source_index.json: L451-L470, L475-L494, L348-L367, L781-L800, L167-L186
.agent/orchestrator/actions_schema.json: L7-L26, L54-L73, L57-L76, L41-L60, L44-L63
.agent/orchestrator/artifact_store.py: L7-L26, L12-L31, L20-L32, L15-L32, L19-L32
.agent/orchestrator/artifact_validator.py: L180-L199, L140-L159, L72-L91, L152-L171, L106-L125
.agent/orchestrator/browser_research.py: L10-L29, L12-L31, L3-L22, L14-L33, L2-L21
.agent/orchestrator/capability_registry.py: L166-L173, L167-L173, L165-L173, L105-L124, L100-L119
.agent/orchestrator/command_runner.py: L6-L25, L7-L26, L12-L31, L9-L28, L18-L37
.agent/orchestrator/config.json: L47-L66, L15-L34, L19-L38, L20-L39, L26-L45
.agent/orchestrator/context_compactor.py: L86-L92, L12-L31, L3-L22, L72-L91, L22-L41
.agent/orchestrator/context_pruner.py: L6-L25, L12-L31, L65-L84, L32-L51, L107-L126
.agent/orchestrator/copyright_guard.py: L7-L26, L3-L22, L9-L28, L2-L21, L1-L20
.agent/orchestrator/file_writer.py: L64-L83, L80-L99, L97-L102, L25-L44, L34-L53
.agent/orchestrator/graph.py: L6-L25, L7-L26, L1-L18, L1-L20, L15-L34
.agent/orchestrator/hooks.py: L3-L22, L21-L37
.agent/orchestrator/kobold_client.py: L14-L33, L69-L77, L17-L36, L66-L77, L71-L77
.agent/orchestrator/page_extractor.py: L74-L93, L23-L42, L88-L97, L81-L97, L21-L40
.agent/orchestrator/patch_applier.py: L47-L66, L84-L103, L50-L69, L62-L81, L57-L76
.agent/orchestrator/playwright_research.py: L14-L33, L7-L26, L12-L31, L9-L28, L53-L72
.agent/orchestrator/prompt_compiler.py: L14-L33, L3-L22, L32-L51, L2-L21, L56-L70
.agent/orchestrator/research_client.py: L30-L49, L64-L83, L65-L84, L58-L77, L36-L55
.agent/orchestrator/response_parser.py: L6-L25, L247-L266, L249-L268, L89-L108, L19-L38
.agent/orchestrator/retry_engine.py: L30-L49, L55-L74, L18-L37, L35-L54, L56-L75
.agent/orchestrator/role_loader.py: L23-L42, L18-L37, L32-L51, L2-L21, L55-L73
.agent/orchestrator/safety_guard.py: L72-L91, L47-L66, L106-L125, L33-L52, L80-L99
.agent/orchestrator/search_result_parser.py: L43-L62, L65-L84, L108-L127, L80-L99, L44-L63
.agent/orchestrator/session_router.py: L50-L69, L79-L98, L80-L99, L125-L135, L2-L21
.agent/orchestrator/skill_registry.py: L47-L66, L84-L103, L62-L81, L25-L44, L92-L111
.agent/orchestrator/source_indexer.py: L12-L31, L3-L22, L4-L23, L23-L42, L50-L69
.agent/orchestrator/state_store.py: L58-L77, L79-L98, L80-L99, L104-L123, L160-L179
.agent/orchestrator/studio_loop.py: L451-L470, L502-L521, L794-L813, L746-L765, L804-L823
.agent/orchestrator/transition_engine.py: L7-L26, L26-L45, L28-L47
.agent/orchestrator/templates/stage_prompt.md: L10-L29, L3-L22, L9-L28, L1-L15, L80-L99
.agent/orchestrator/__pycache__/artifact_store.cpython-312.pyc: L1-L18, L21-L28, L2-L21
.agent/orchestrator/__pycache__/artifact_store.cpython-314.pyc: L1-L19, L1-L17, L16-L29
.agent/orchestrator/__pycache__/artifact_validator.cpython-312.pyc: L3-L22, L1-L17, L40-L59, L86-L95, L39-L58
.agent/orchestrator/__pycache__/artifact_validator.cpython-314.pyc: L1-L18, L3-L22, L70-L89, L35-L54, L33-L52
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc: L14-L33, L84-L103, L117-L136, L120-L139, L118-L137
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc.2709833153488: L7-L26, L84-L103, L50-L69, L85-L104, L41-L60
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc: L12-L31, L154-L173, L35-L54, L33-L52, L153-L172
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc.3073430176800: L64-L83, L9-L28, L32-L51, L31-L50, L29-L48
.agent/orchestrator/__pycache__/capability_registry.cpython-312.pyc: L12-L31, L31-L50
.agent/orchestrator/__pycache__/capability_registry.cpython-314.pyc: L44-L63
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-312.pyc: L12-L31, L1-L17, L48-L60
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-314.pyc: L6-L25, L39-L49, L1-L18
.agent/orchestrator/__pycache__/command_runner.cpython-312.pyc: L51-L63, L1-L20
.agent/orchestrator/__pycache__/command_runner.cpython-314.pyc: L16-L35, L52-L68, L1-L20
.agent/orchestrator/__pycache__/context_compactor.cpython-312.pyc: L1-L19, L1-L18, L48-L67, L3-L22
.agent/orchestrator/__pycache__/context_compactor.cpython-314.pyc: L1-L19, L1-L18, L49-L68, L3-L22
.agent/orchestrator/__pycache__/context_pruner.cpython-312.pyc: L10-L29, L1-L18, L35-L54, L21-L40, L34-L53
.agent/orchestrator/__pycache__/context_pruner.cpython-314.pyc: L10-L29, L1-L18, L33-L52, L62-L81, L20-L39
.agent/orchestrator/__pycache__/copyright_guard.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/copyright_guard.cpython-314.pyc: L1-L20
.agent/orchestrator/__pycache__/file_writer.cpython-312.pyc: L30-L49, L32-L51, L1-L20, L15-L34, L17-L36
.agent/orchestrator/__pycache__/file_writer.cpython-314.pyc: L18-L37, L2-L21, L1-L20, L31-L50, L17-L36
.agent/orchestrator/__pycache__/graph.cpython-312.pyc: L13-L23, L4-L23, L8-L23, L2-L21, L7-L23
.agent/orchestrator/__pycache__/graph.cpython-314.pyc: L10-L29, L7-L26, L18-L37, L9-L28, L1-L20
.agent/orchestrator/__pycache__/hooks.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/hooks.cpython-314.pyc: L1-L16
.agent/orchestrator/__pycache__/kobold_client.cpython-312.pyc: L1-L19, L1-L17
.agent/orchestrator/__pycache__/kobold_client.cpython-314.pyc: L1-L18, L2-L21, L1-L20
.agent/orchestrator/__pycache__/page_extractor.cpython-312.pyc: L36-L55, L34-L53, L2-L21, L1-L20
.agent/orchestrator/__pycache__/page_extractor.cpython-314.pyc: L1-L19, L32-L51, L34-L53
.agent/orchestrator/__pycache__/patch_applier.cpython-312.pyc: L7-L26, L4-L23, L1-L17, L55-L60, L22-L41
.agent/orchestrator/__pycache__/patch_applier.cpython-314.pyc: L18-L37, L4-L23, L22-L41, L1-L20, L1-L16
.agent/orchestrator/__pycache__/playwright_research.cpython-312.pyc: L1-L19, L1-L18, L14-L33
.agent/orchestrator/__pycache__/playwright_research.cpython-314.pyc: L1-L19, L14-L33, L1-L20
.agent/orchestrator/__pycache__/prompt_compiler.cpython-312.pyc: L14-L33, L10-L29, L1-L18, L11-L30, L1-L19
.agent/orchestrator/__pycache__/prompt_compiler.cpython-314.pyc: L12-L31, L1-L18, L23-L42, L11-L30, L1-L19
.agent/orchestrator/__pycache__/research_client.cpython-312.pyc: L1-L19, L5-L24, L13-L32
.agent/orchestrator/__pycache__/research_client.cpython-314.pyc: L6-L25, L14-L33, L1-L18, L32-L51, L1-L20
.agent/orchestrator/__pycache__/response_parser.cpython-312.pyc: L1-L17, L16-L35
.agent/orchestrator/__pycache__/response_parser.cpython-314.pyc: L18-L37, L1-L16, L94-L113, L97-L115
.agent/orchestrator/__pycache__/retry_engine.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/retry_engine.cpython-314.pyc: L63-L82, L1-L16, L56-L75, L79-L98
.agent/orchestrator/__pycache__/role_loader.cpython-312.pyc: L6-L25, L3-L22, L4-L23, L9-L28, L8-L27
.agent/orchestrator/__pycache__/role_loader.cpython-314.pyc: L6-L25, L7-L26, L4-L23
.agent/orchestrator/__pycache__/safety_guard.cpython-312.pyc: L6-L25, L39-L55, L4-L23, L22-L41, L28-L47
.agent/orchestrator/__pycache__/safety_guard.cpython-314.pyc: L38-L54, L4-L23, L21-L40, L5-L24, L20-L39
.agent/orchestrator/__pycache__/search_result_parser.cpython-312.pyc: L19-L38, L1-L17
.agent/orchestrator/__pycache__/search_result_parser.cpython-314.pyc: L1-L16, L22-L41
.agent/orchestrator/__pycache__/session_router.cpython-312.pyc: L10-L29, L30-L49, L4-L23, L36-L55, L31-L50
.agent/orchestrator/__pycache__/session_router.cpython-314.pyc: L23-L42, L3-L22, L2-L21, L22-L41, L20-L39
.agent/orchestrator/__pycache__/skill_registry.cpython-312.pyc: L6-L25, L7-L26, L12-L31, L54-L61, L22-L41
.agent/orchestrator/__pycache__/skill_registry.cpython-314.pyc: L10-L29, L23-L42, L3-L22, L4-L23, L2-L21
.agent/orchestrator/__pycache__/source_indexer.cpython-312.pyc: L10-L29, L23-L42, L1-L18, L1-L20, L1-L19
.agent/orchestrator/__pycache__/source_indexer.cpython-314.pyc: L10-L29, L1-L18, L1-L17, L20-L39, L1-L19
.agent/orchestrator/__pycache__/source_summarizer.cpython-312.pyc: L1-L7
.agent/orchestrator/__pycache__/state_store.cpython-312.pyc: L9-L28, L99-L118, L36-L55, L35-L54, L108-L127
.agent/orchestrator/__pycache__/state_store.cpython-314.pyc: L30-L49, L4-L23, L99-L118, L112-L131, L118-L137
.agent/orchestrator/__pycache__/studio_loop.cpython-312.pyc: L115-L134, L50-L69, L41-L60, L22-L41, L54-L73
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc: L72-L91, L278-L297, L276-L295, L135-L154, L212-L231
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc.3098252610704: L58-L77, L135-L154, L106-L125, L56-L75, L45-L64
.agent/orchestrator/__pycache__/test_runner.cpython-312.pyc: L1-L18
.agent/orchestrator/__pycache__/test_runner.cpython-314.pyc: L1-L18
.agent/orchestrator/__pycache__/transition_engine.cpython-312.pyc: L7-L26, L1-L17
.agent/orchestrator/__pycache__/transition_engine.cpython-314.pyc: L1-L16, L2-L21
.agent/orchestrator/__pycache__/web_fetcher.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/web_research.cpython-312.pyc: L1-L17
.agent/skills/asset_creator_skills.md: L33-L43
.agent/skills/designer_skills.md: L22-L41, L15-L34, L25-L44, L8-L27, L51-L60
.agent/skills/developer_skills.md: L57-L63, L58-L63, L52-L63, L48-L63, L51-L63
.agent/skills/producer_skills.md: L27-L46, L41-L48
.agent/skills/qa_skills.md: L22-L41, L39-L48, L37-L48, L21-L40, L17-L36
.agent/skills/registry.json: L5-L13, L3-L13, L2-L13, L4-L13, L6-L13
.agent/skills/researcher_skills.md: L10-L29, L58-L77, L87-L97, L1-L15, L35-L54
.agent/skills/asset_creator/skill.json: L2-L15, L4-L15, L1-L15
.agent/skills/asset_creator/SKILL.md: L1-L3
.agent/skills/bug_hunter/skill.json: L2-L20, L1-L16, L1-L17, L6-L20
.agent/skills/bug_hunter/SKILL.md: L1-L3
.agent/skills/debug_dev/skill.json: L2-L15, L4-L15, L1-L15
.agent/skills/debug_dev/SKILL.md: L1-L3
.agent/skills/designer/skill.json: L2-L20, L1-L16, L1-L17, L6-L20
.agent/skills/designer/SKILL.md: L1-L3
.agent/skills/developer/skill.json: L2-L15, L4-L15, L1-L15
.agent/skills/developer/SKILL.md: L1-L3
.agent/skills/producer/skill.json: L2-L20, L1-L16, L1-L17, L6-L20
.agent/skills/producer/SKILL.md: L1-L3
.agent/skills/qa/skill.json: L2-L20, L1-L16, L1-L17, L6-L20
.agent/skills/qa/SKILL.md: L1-L3
.agent/skills/researcher/skill.json: L1-L17, L2-L21, L15-L21, L8-L21, L1-L16
.agent/skills/researcher/SKILL.md: L1-L3
.agent/workflows/asset_creator.md: L3-L22, L19-L38, L25-L42, L35-L42
.agent/workflows/bug_hunter.md: L33-L40, L4-L23, L21-L40
.agent/workflows/concept_producer.md: L33-L51, L44-L51, L4-L23, L32-L51
.agent/workflows/debug_dev.md: L34-L41, L4-L23
.agent/workflows/designer.md: L23-L42, L3-L22, L28-L43, L36-L43, L17-L36
.agent/workflows/developer.md: L10-L29, L3-L22, L54-L61, L47-L61, L40-L59
.agent/workflows/qa_tester.md: L3-L22, L20-L39, L53-L60, L21-L40
.agent/workflows/researcher.md: L10-L29, L12-L31, L1-L18, L3-L22, L54-L61
.agent/workflows/STUDIO_LOOP_WORKFLOW.md: L14-L33, L23-L42, L3-L22, L1-L18, L18-L37
.agent/workflows/task_template.md: L10-L29, L12-L31, L30-L49, L22-L41, L21-L40
docs/local_setup.md: L10-L29, L1-L17, L2-L21, L36-L55, L58-L63
docs/verification/browser_research_mdn_requestanimationframe.md: L37-L53, L28-L47, L22-L41, L31-L50
tests/e2e_loop_test.py: L47-L66, L140-L148, L63-L82, L56-L75, L87-L106
tests/real_browser_research_check.py: L3-L22, L32-L51, L35-L54, L33-L52, L37-L56
tests/regression_page_extractor.py: L1-L18
tests/test_autonomous_loop.py: L33-L52, L80-L99, L57-L76, L25-L44, L10-L29
tests/test_browser_research_mock.py: L174-L190, L80-L99, L62-L81, L166-L185, L105-L124
tests/test_kobold_client.py: L23-L42, L4-L23, L11-L30
tests/test_repair_prompt.py: L121-L140, L41-L60, L190-L209, L224-L243, L200-L219
tests/test_response_parser.py: L135-L154, L108-L127, L56-L75, L92-L111, L10-L29
tests/test_robustness.py: L72-L91, L47-L66, L84-L103, L37-L56, L45-L64
tests/test_sessions_and_skills.py: L140-L159, L115-L134, L169-L188, L214-L233, L84-L103
tests/__pycache__/test_browser_research_mock.cpython-314.pyc: L74-L93, L23-L42, L29-L48, L75-L94, L5-L24
tests/__pycache__/test_repair_prompt.cpython-314.pyc: L64-L83, L55-L74, L4-L23, L1-L17, L58-L77
tests/__pycache__/test_response_parser.cpython-314.pyc: L36-L55, L42-L61, L31-L50, L78-L97, L96-L115
tests/__pycache__/test_robustness.cpython-314.pyc: L1-L19, L12-L31, L8-L27
tools/bootstrap_local_env.py: L48-L67, L47-L66, L97-L116, L78-L97
tools/bundle_project.py: L47-L66, L50-L69, L57-L76, L45-L64, L34-L53
tools/check_perms.py: L3-L22, L1-L18, L2-L21, L12-L25, L1-L20
tools/context_culler.py: L50-L69, L33-L52, L62-L81, L98-L104, L45-L64
tools/find_bloat.py: L23-L42, L1-L17, L33-L45, L1-L20, L17-L36
tools/test_orchestrator.py: L115-L134, L47-L66, L96-L115, L56-L75, L123-L135
tools/verify_clean_runtime.py: L226-L245, L249-L268, L252-L271, L253-L272, L108-L127
tools/__pycache__/verify_clean_runtime.cpython-314.pyc: L10-L29, L66-L78, L3-L22, L50-L69, L35-L54

