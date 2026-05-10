# Context Pack: improve_the_studio_loop_harness_by_adding_a_safe / concept_producer

## Feature Goal
Improve the Studio Loop harness by adding a safer local-codebase audit path for researcher stages and reducing prompt bloat. Keep changes small and verify with tests.

## Current Stage
concept_producer

## Decision Memory
Refer to .agent/Loop_Flow/context_packs/improve_the_studio_loop_harness_by_adding_a_safe_decision_memory.md for stable decisions and constraints.

## Relevant Artifacts
{}

## Relevant Research Briefs
No research results available yet.

## Validation Status
[]

## Pruned Source Context
--- Context Pruning Map for: ['improve', 'studio', 'loop', 'harness', 'adding', 'safer', 'local-codebase', 'audit', 'path', 'researcher', 'stages', 'concept_producer'] ---
ai_harness_bundle.txt: L66-L85, L68-L87, L627-L646, L1911-L1930, L1743-L1762
bundle_harness.bat: L49-L68, L66-L85, L42-L61, L85-L101, L72-L91
HANDOFF_SCHEMA.json: L64-L83, L17-L36, L1-L19, L34-L53, L80-L99
package-lock.json: L471-L490, L928-L947, L1-L16, L487-L506, L930-L949
package.json: L1-L14
README.md: L20-L33, L1-L15, L1-L17, L12-L31, L3-L22
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither.go: L363-L382
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/parallel.go: L27-L46
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/.github/workflows/test.yml: L4-L23, L1-L19
.agent/Loop_Flow/.gitkeep: Full File
.agent/Loop_Flow/source_index.json: L366-L385, L854-L873, L138-L157, L169-L188, L849-L868
.agent/orchestrator/actions_schema.json: L50-L69, L7-L26, L60-L79, L63-L82, L6-L25
.agent/orchestrator/artifact_store.py: L20-L32, L7-L26, L15-L32, L5-L24, L12-L31
.agent/orchestrator/artifact_validator.py: L109-L128, L120-L139, L71-L90, L193-L212, L226-L234
.agent/orchestrator/browser_research.py: L337-L356, L70-L89, L2-L21, L14-L33, L89-L108
.agent/orchestrator/capability_registry.py: L165-L173, L100-L119, L167-L173, L166-L173, L105-L124
.agent/orchestrator/command_runner.py: L13-L32, L69-L88, L9-L28, L7-L26, L101-L107
.agent/orchestrator/config.json: L15-L34, L26-L45, L20-L39, L19-L38, L47-L66
.agent/orchestrator/context_compactor.py: L13-L32, L56-L75, L72-L91, L46-L65, L22-L41
.agent/orchestrator/context_pruner.py: L13-L32, L56-L75, L1-L18, L66-L85, L114-L133
.agent/orchestrator/copyright_guard.py: L2-L21, L65-L72, L1-L20, L9-L28, L7-L26
.agent/orchestrator/file_writer.py: L90-L102, L42-L61, L97-L102, L71-L90, L64-L83
.agent/orchestrator/graph.py: L13-L32, L1-L18, L31-L42, L15-L34, L36-L42
.agent/orchestrator/hooks.py: L3-L22, L21-L37
.agent/orchestrator/kobold_client.py: L14-L33, L66-L77, L69-L77, L17-L36, L71-L77
.agent/orchestrator/page_extractor.py: L88-L97, L80-L97, L21-L40, L81-L97, L74-L93
.agent/orchestrator/patch_applier.py: L57-L76, L1-L19, L84-L103, L99-L109, L11-L30
.agent/orchestrator/playwright_research.py: L14-L33, L15-L34, L9-L28, L7-L26, L53-L72
.agent/orchestrator/prompt_compiler.py: L41-L60, L42-L61, L15-L34, L35-L54, L46-L65
.agent/orchestrator/research_client.py: L151-L170, L281-L300, L227-L246, L361-L380, L193-L212
.agent/orchestrator/response_parser.py: L247-L266, L253-L272, L89-L108, L284-L303, L338-L357
.agent/orchestrator/retry_engine.py: L66-L85, L68-L87, L67-L86, L22-L41, L40-L59
.agent/orchestrator/role_loader.py: L13-L32, L28-L47, L2-L21, L32-L51, L31-L50
.agent/orchestrator/safety_guard.py: L66-L85, L68-L87, L42-L61, L72-L91, L71-L90
.agent/orchestrator/search_result_parser.py: L80-L99, L108-L127, L43-L62, L44-L63, L65-L84
.agent/orchestrator/session_router.py: L119-L135, L79-L98, L125-L135, L17-L36, L11-L30
.agent/orchestrator/skill_registry.py: L49-L68, L66-L85, L71-L90, L95-L113, L17-L36
.agent/orchestrator/source_indexer.py: L28-L47, L35-L54, L29-L48, L70-L79, L50-L69
.agent/orchestrator/state_store.py: L127-L146, L79-L98, L94-L113, L95-L114, L28-L47
.agent/orchestrator/studio_loop.py: L901-L920, L66-L85, L42-L61, L281-L300, L477-L496
.agent/orchestrator/transition_engine.py: L28-L47, L7-L26, L27-L46, L5-L24, L8-L27
.agent/orchestrator/templates/stage_prompt.md: L102-L121, L35-L54, L1-L15, L9-L28, L27-L46
.agent/orchestrator/__pycache__/artifact_store.cpython-312.pyc: L21-L28, L1-L18, L2-L21
.agent/orchestrator/__pycache__/artifact_store.cpython-314.pyc: L16-L29, L1-L17, L1-L19
.agent/orchestrator/__pycache__/artifact_validator.cpython-312.pyc: L1-L17, L38-L57, L40-L59, L39-L58, L3-L22
.agent/orchestrator/__pycache__/artifact_validator.cpython-314.pyc: L1-L18, L91-L110, L46-L65, L108-L127, L7-L26
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc: L13-L32, L15-L34, L14-L33, L117-L136, L120-L139
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc.2709833153488: L86-L105, L85-L104, L41-L60, L50-L69, L87-L106
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc: L156-L175, L154-L173, L153-L172, L155-L174, L123-L142
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc.3073430176800: L32-L51, L31-L50, L29-L48, L64-L83, L9-L28
.agent/orchestrator/__pycache__/capability_registry.cpython-312.pyc: L12-L31, L31-L50
.agent/orchestrator/__pycache__/capability_registry.cpython-314.pyc: L44-L63
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-312.pyc: L1-L17, L12-L31, L48-L60
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-314.pyc: L1-L18, L6-L25, L39-L49
.agent/orchestrator/__pycache__/command_runner.cpython-312.pyc: L1-L20, L51-L63
.agent/orchestrator/__pycache__/command_runner.cpython-314.pyc: L52-L68, L1-L20, L16-L35
.agent/orchestrator/__pycache__/context_compactor.cpython-312.pyc: L48-L67, L1-L18, L3-L22, L1-L19
.agent/orchestrator/__pycache__/context_compactor.cpython-314.pyc: L49-L68, L1-L18, L3-L22, L1-L19
.agent/orchestrator/__pycache__/context_pruner.cpython-312.pyc: L1-L18, L65-L77, L10-L29, L34-L53, L35-L54
.agent/orchestrator/__pycache__/context_pruner.cpython-314.pyc: L15-L34, L1-L16, L59-L78, L39-L58, L25-L44
.agent/orchestrator/__pycache__/copyright_guard.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/copyright_guard.cpython-314.pyc: L1-L20
.agent/orchestrator/__pycache__/file_writer.cpython-312.pyc: L17-L36, L32-L51, L15-L34, L29-L48, L1-L20
.agent/orchestrator/__pycache__/file_writer.cpython-314.pyc: L28-L47, L2-L21, L31-L50, L29-L48, L1-L20
.agent/orchestrator/__pycache__/graph.cpython-312.pyc: L6-L23, L9-L23, L2-L21, L7-L23, L15-L23
.agent/orchestrator/__pycache__/graph.cpython-314.pyc: L13-L32, L15-L34, L1-L20, L9-L28, L7-L26
.agent/orchestrator/__pycache__/hooks.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/hooks.cpython-314.pyc: L1-L16
.agent/orchestrator/__pycache__/kobold_client.cpython-312.pyc: L1-L17, L1-L19
.agent/orchestrator/__pycache__/kobold_client.cpython-314.pyc: L1-L18, L1-L20, L2-L21
.agent/orchestrator/__pycache__/page_extractor.cpython-312.pyc: L34-L53, L1-L20, L36-L55, L2-L21
.agent/orchestrator/__pycache__/page_extractor.cpython-314.pyc: L34-L53, L32-L51, L1-L19
.agent/orchestrator/__pycache__/patch_applier.cpython-312.pyc: L28-L47, L46-L60, L26-L45, L1-L17, L4-L23
.agent/orchestrator/__pycache__/patch_applier.cpython-314.pyc: L48-L67, L1-L20, L4-L23, L22-L41, L1-L16
.agent/orchestrator/__pycache__/playwright_research.cpython-312.pyc: L1-L18, L14-L33, L1-L19
.agent/orchestrator/__pycache__/playwright_research.cpython-314.pyc: L1-L20, L14-L33, L1-L19
.agent/orchestrator/__pycache__/prompt_compiler.cpython-312.pyc: L1-L18, L14-L33, L10-L29, L1-L19, L11-L30
.agent/orchestrator/__pycache__/prompt_compiler.cpython-314.pyc: L1-L18, L31-L50, L29-L48, L26-L45, L1-L17
.agent/orchestrator/__pycache__/research_client.cpython-312.pyc: L13-L32, L5-L24, L1-L19
.agent/orchestrator/__pycache__/research_client.cpython-314.pyc: L42-L61, L120-L139, L78-L97, L20-L39, L1-L19
.agent/orchestrator/__pycache__/response_parser.cpython-312.pyc: L1-L17, L16-L35
.agent/orchestrator/__pycache__/response_parser.cpython-314.pyc: L98-L117, L93-L112, L94-L113, L1-L16, L96-L115
.agent/orchestrator/__pycache__/retry_engine.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/retry_engine.cpython-314.pyc: L102-L121, L72-L91, L103-L122, L1-L16, L74-L93
.agent/orchestrator/__pycache__/role_loader.cpython-312.pyc: L9-L28, L4-L23, L6-L25, L8-L27, L3-L22
.agent/orchestrator/__pycache__/role_loader.cpython-314.pyc: L3-L22, L6-L25, L4-L23, L7-L26
.agent/orchestrator/__pycache__/safety_guard.cpython-312.pyc: L28-L47, L29-L48, L22-L41, L4-L23, L39-L55
.agent/orchestrator/__pycache__/safety_guard.cpython-314.pyc: L1-L19, L26-L45, L4-L23, L27-L46, L5-L24
.agent/orchestrator/__pycache__/search_result_parser.cpython-312.pyc: L1-L17, L19-L38
.agent/orchestrator/__pycache__/search_result_parser.cpython-314.pyc: L1-L16, L22-L41
.agent/orchestrator/__pycache__/session_router.cpython-312.pyc: L31-L50, L29-L48, L118-L128, L30-L49, L4-L23
.agent/orchestrator/__pycache__/session_router.cpython-314.pyc: L2-L21, L29-L48, L9-L28, L22-L41, L5-L24
.agent/orchestrator/__pycache__/skill_registry.cpython-312.pyc: L54-L61, L22-L41, L7-L26, L36-L55, L12-L31
.agent/orchestrator/__pycache__/skill_registry.cpython-314.pyc: L48-L58, L2-L21, L42-L58, L4-L23, L36-L55
.agent/orchestrator/__pycache__/source_indexer.cpython-312.pyc: L1-L18, L1-L19, L1-L20, L10-L29, L8-L27
.agent/orchestrator/__pycache__/source_indexer.cpython-314.pyc: L1-L18, L1-L19, L1-L17, L10-L29, L20-L39
.agent/orchestrator/__pycache__/source_summarizer.cpython-312.pyc: L1-L7
.agent/orchestrator/__pycache__/state_store.cpython-312.pyc: L97-L116, L116-L135, L108-L127, L9-L28, L110-L129
.agent/orchestrator/__pycache__/state_store.cpython-314.pyc: L112-L131, L102-L121, L29-L48, L109-L128, L4-L23
.agent/orchestrator/__pycache__/studio_loop.cpython-312.pyc: L42-L61, L183-L202, L19-L38, L176-L195, L112-L131
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc: L285-L304, L360-L379, L57-L76, L168-L187, L72-L91
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc.3098252610704: L71-L90, L172-L191, L45-L64, L19-L38, L106-L125
.agent/orchestrator/__pycache__/test_runner.cpython-312.pyc: L1-L18
.agent/orchestrator/__pycache__/test_runner.cpython-314.pyc: L1-L18
.agent/orchestrator/__pycache__/transition_engine.cpython-312.pyc: L1-L17, L4-L23, L7-L26
.agent/orchestrator/__pycache__/transition_engine.cpython-314.pyc: L1-L16, L1-L20, L2-L21
.agent/orchestrator/__pycache__/web_fetcher.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/web_research.cpython-312.pyc: L1-L17
.agent/skills/asset_creator_skills.md: L33-L43
.agent/skills/designer_skills.md: L15-L34, L22-L41, L51-L60, L8-L27, L25-L44
.agent/skills/developer_skills.md: L57-L63, L51-L63, L52-L63, L48-L63, L58-L63
.agent/skills/producer_skills.md: L27-L46, L41-L48
.agent/skills/qa_skills.md: L26-L45, L22-L41, L39-L48, L17-L36, L21-L40
.agent/skills/registry.json: L3-L13, L4-L13, L1-L13, L5-L13, L6-L13
.agent/skills/researcher_skills.md: L1-L15, L1-L20, L58-L77, L1-L16, L10-L29
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
.agent/skills/producer/skill.json: L1-L17, L6-L20, L1-L16, L2-L20, L1-L19
.agent/skills/producer/SKILL.md: L1-L3
.agent/skills/qa/skill.json: L1-L16, L1-L17, L2-L20, L6-L20
.agent/skills/qa/SKILL.md: L1-L3
.agent/skills/researcher/skill.json: L2-L21, L6-L21, L13-L21, L10-L21, L1-L17
.agent/skills/researcher/SKILL.md: L1-L3
.agent/workflows/asset_creator.md: L35-L42, L3-L22, L25-L42, L19-L38
.agent/workflows/bug_hunter.md: L33-L40, L21-L40, L4-L23
.agent/workflows/concept_producer.md: L44-L51, L32-L51, L4-L23, L33-L51
.agent/workflows/debug_dev.md: L34-L41, L4-L23
.agent/workflows/designer.md: L28-L43, L36-L43, L17-L36, L24-L43, L3-L22
.agent/workflows/developer.md: L40-L59, L10-L29, L56-L63, L34-L53, L3-L22
.agent/workflows/qa_tester.md: L60-L67, L3-L22, L21-L40, L20-L39
.agent/workflows/researcher.md: L54-L61, L1-L18, L27-L46, L1-L16, L39-L58
.agent/workflows/STUDIO_LOOP_WORKFLOW.md: L17-L36, L61-L80, L1-L18, L62-L81, L14-L33
.agent/workflows/task_template.md: L13-L32, L47-L54, L15-L34, L22-L41, L10-L29
docs/local_setup.md: L2-L21, L1-L17, L36-L55, L58-L63, L50-L63
docs/verification/browser_research_mdn_requestanimationframe.md: L28-L47, L37-L53, L22-L41, L31-L50
tests/e2e_loop_test.py: L122-L141, L66-L85, L88-L107, L71-L90, L19-L38
tests/real_browser_research_check.py: L41-L60, L32-L51, L35-L54, L37-L56, L33-L52
tests/regression_page_extractor.py: L1-L18
tests/test_autonomous_loop.py: L66-L85, L68-L87, L42-L61, L57-L76, L78-L97
tests/test_browser_research_mock.py: L174-L190, L95-L114, L113-L132, L112-L131, L80-L99
tests/test_gemma4_factory_tuning.py: L1-L20, L35-L51
tests/test_kobold_client.py: L23-L42, L4-L23, L11-L30
tests/test_local_codebase_audit.py: L151-L170, L431-L450, L42-L61, L281-L300, L227-L246
tests/test_repair_prompt.py: L68-L87, L57-L76, L109-L128, L200-L219, L172-L191
tests/test_response_parser.py: L277-L296, L230-L249, L339-L358, L227-L246, L200-L219
tests/test_robustness.py: L42-L61, L91-L105, L72-L91, L78-L97, L37-L56
tests/test_sessions_and_skills.py: L49-L68, L168-L187, L183-L202, L169-L188, L45-L64
tests/__pycache__/test_browser_research_mock.cpython-314.pyc: L29-L48, L75-L94, L5-L24, L74-L93, L23-L42
tests/__pycache__/test_repair_prompt.cpython-314.pyc: L151-L170, L64-L83, L84-L103, L102-L121, L152-L171
tests/__pycache__/test_response_parser.cpython-314.pyc: L42-L61, L31-L50, L22-L41, L78-L97, L36-L55
tests/__pycache__/test_robustness.cpython-314.pyc: L14-L33, L65-L82, L10-L29, L3-L22, L62-L81
tools/bootstrap_local_env.py: L48-L67, L47-L66, L78-L97, L97-L116
tools/bundle_project.py: L68-L87, L57-L76, L45-L64, L34-L53, L2-L21
tools/check_perms.py: L1-L18, L2-L21, L1-L20, L7-L25, L5-L24
tools/context_culler.py: L66-L85, L45-L64, L17-L36, L34-L53, L11-L30
tools/find_bloat.py: L17-L36, L33-L45, L1-L20, L1-L17, L19-L38
tools/test_orchestrator.py: L49-L68, L66-L85, L71-L90, L121-L135, L125-L135
tools/verify_clean_runtime.py: L127-L146, L277-L296, L230-L249, L227-L246, L210-L229
tools/__pycache__/verify_clean_runtime.cpython-314.pyc: L28-L47, L76-L89, L74-L89, L40-L59, L37-L56
tools/__pycache__/__init__.cpython-314.pyc: L1-L2

