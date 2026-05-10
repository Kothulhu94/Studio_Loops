# Context Pack: improve_the_studio_loop_harness_by_adding_a_safe / developer

## Feature Goal
Improve the Studio Loop harness by adding a safer local-codebase audit path for researcher stages and reducing prompt bloat. Keep changes small and verify with tests.

## Current Stage
developer

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
--- Context Pruning Map for: ['improve', 'studio', 'loop', 'harness', 'adding', 'safer', 'local-codebase', 'audit', 'path', 'researcher', 'stages', 'developer', 'improve_the_studio_loop_harness_by_adding_a_safe_researcher_perform_a_technical_audit_of_t_research_brief.md', 'perform', 'technical', 'specifically', 'complete'] ---
ai_harness_bundle.txt: L1807-L1826, L1879-L1898, L34-L53, L137-L156, L1690-L1709
bundle_harness.bat: L50-L69, L23-L42, L49-L68, L64-L83, L8-L27
HANDOFF_SCHEMA.json: L50-L69, L23-L42, L34-L53, L1-L20, L96-L115
package-lock.json: L3-L22, L487-L506, L1211-L1230, L1-L16, L930-L949
package.json: L1-L14
README.md: L12-L31, L3-L22, L1-L17, L26-L33, L1-L15
.agent/bin/licenses/cloud.google.com/go/compute/metadata/LICENSE: L66-L85
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/.gitignore: L100-L105, L1-L20, L20-L39, L1-L19
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/dither.go: L363-L382
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/LICENSE: L266-L285, L311-L330, L91-L110
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/parallel.go: L27-L46
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/README.md: L1-L20, L102-L121
.agent/bin/licenses/github.com/makeworld-the-better-one/dither/v2/.github/workflows/test.yml: L4-L23, L1-L19
.agent/bin/licenses/github.com/minio/selfupdate/LICENSE: L66-L85
.agent/bin/licenses/github.com/spf13/afero/LICENSE.txt: L65-L84
.agent/bin/licenses/github.com/spf13/cobra/LICENSE.txt: L65-L84
.agent/bin/licenses/github.com/TheZoraiz/ascii-image-converter/LICENSE.txt: L66-L85
.agent/Loop_Flow/.gitkeep: Full File
.agent/Loop_Flow/autonomous_loop_refinement_blueprint.md: L5-L15, L3-L15, L1-L15
.agent/Loop_Flow/context_map.json: Full File
.agent/Loop_Flow/improve_the_studio_loop_harness_by_adding_a_safe_blueprint.md: L3-L22, L15-L34, L11-L30, L38-L43, L1-L15
.agent/Loop_Flow/source_index.json: L770-L789, L285-L304, L559-L578, L731-L750, L366-L385
.agent/orchestrator/actions_schema.json: L10-L29, L50-L69, L35-L54, L7-L26, L63-L82
.agent/orchestrator/artifact_store.py: L12-L31, L18-L32, L7-L26, L19-L32, L15-L32
.agent/orchestrator/artifact_validator.py: L161-L180, L222-L234, L170-L189, L34-L53, L1-L20
.agent/orchestrator/browser_research.py: L10-L29, L355-L364, L337-L356, L64-L83, L339-L358
.agent/orchestrator/capability_registry.py: L41-L60, L165-L173, L167-L173, L105-L124, L140-L159
.agent/orchestrator/command_runner.py: L101-L107, L12-L31, L18-L37, L13-L32, L7-L26
.agent/orchestrator/config.json: L26-L45, L20-L39, L15-L34, L19-L38, L40-L59
.agent/orchestrator/context_compactor.py: L72-L91, L12-L31, L3-L22, L13-L32, L22-L41
.agent/orchestrator/context_pruner.py: L39-L58, L72-L91, L89-L108, L3-L22, L13-L32
.agent/orchestrator/copyright_guard.py: L65-L72, L3-L22, L7-L26, L1-L20, L2-L21
.agent/orchestrator/file_writer.py: L88-L102, L13-L32, L34-L53, L84-L102, L40-L59
.agent/orchestrator/graph.py: L6-L25, L13-L32, L7-L26, L15-L34, L1-L20
.agent/orchestrator/hooks.py: L21-L37, L3-L22
.agent/orchestrator/kobold_client.py: L71-L77, L14-L33, L16-L35, L66-L77, L17-L36
.agent/orchestrator/page_extractor.py: L23-L42, L21-L40, L88-L97, L24-L43, L74-L93
.agent/orchestrator/patch_applier.py: L10-L29, L50-L69, L91-L109, L57-L76, L11-L30
.agent/orchestrator/playwright_research.py: L12-L31, L7-L26, L14-L33, L15-L34, L16-L35
.agent/orchestrator/prompt_compiler.py: L39-L58, L43-L62, L72-L89, L12-L31, L3-L22
.agent/orchestrator/research_client.py: L350-L369, L34-L53, L399-L418, L478-L497, L215-L234
.agent/orchestrator/response_parser.py: L20-L39, L352-L371, L284-L303, L89-L108, L351-L370
.agent/orchestrator/retry_engine.py: L20-L39, L23-L42, L45-L64, L24-L43, L35-L54
.agent/orchestrator/role_loader.py: L31-L50, L23-L42, L56-L73, L32-L51, L24-L43
.agent/orchestrator/safety_guard.py: L116-L135, L67-L86, L97-L116, L114-L133, L81-L100
.agent/orchestrator/search_result_parser.py: L44-L63, L65-L84, L108-L127, L59-L78, L80-L99
.agent/orchestrator/session_router.py: L10-L29, L20-L39, L11-L30, L40-L59, L81-L100
.agent/orchestrator/skill_registry.py: L67-L86, L49-L68, L40-L59, L92-L111, L8-L27
.agent/orchestrator/source_indexer.py: L50-L69, L23-L42, L24-L43, L12-L31, L3-L22
.agent/orchestrator/state_store.py: L128-L147, L10-L29, L97-L116, L167-L186, L8-L27
.agent/orchestrator/studio_loop.py: L397-L416, L420-L439, L57-L76, L399-L418, L40-L59
.agent/orchestrator/transition_engine.py: L21-L40, L38-L57, L7-L26, L41-L60, L55-L69
.agent/orchestrator/templates/stage_prompt.md: L10-L29, L93-L112, L3-L22, L27-L46, L35-L54
.agent/orchestrator/__pycache__/artifact_store.cpython-312.pyc: L1-L18, L21-L28, L2-L21
.agent/orchestrator/__pycache__/artifact_store.cpython-314.pyc: L1-L17, L1-L19, L16-L29
.agent/orchestrator/__pycache__/artifact_validator.cpython-312.pyc: L39-L58, L38-L57, L3-L22, L1-L17, L2-L21
.agent/orchestrator/__pycache__/artifact_validator.cpython-314.pyc: L45-L64, L6-L25, L7-L26, L41-L60, L4-L23
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc: L84-L103, L118-L137, L13-L32, L44-L63, L14-L33
.agent/orchestrator/__pycache__/browser_research.cpython-312.pyc.2709833153488: L50-L69, L45-L64, L42-L61, L84-L103, L85-L104
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc: L26-L45, L154-L173, L12-L31, L35-L54, L22-L41
.agent/orchestrator/__pycache__/browser_research.cpython-314.pyc.3073430176800: L39-L58, L31-L50, L32-L51, L61-L80, L63-L82
.agent/orchestrator/__pycache__/capability_registry.cpython-312.pyc: L31-L50, L10-L29, L12-L31
.agent/orchestrator/__pycache__/capability_registry.cpython-314.pyc: L44-L63, L10-L29
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-312.pyc: L1-L17, L48-L60, L12-L31
.agent/orchestrator/__pycache__/chrome_devtools_research.cpython-314.pyc: L1-L18, L39-L49, L6-L25
.agent/orchestrator/__pycache__/command_runner.cpython-312.pyc: L1-L20, L51-L63
.agent/orchestrator/__pycache__/command_runner.cpython-314.pyc: L16-L35, L1-L20, L52-L68
.agent/orchestrator/__pycache__/context_compactor.cpython-312.pyc: L48-L67, L1-L18, L1-L19, L3-L22
.agent/orchestrator/__pycache__/context_compactor.cpython-314.pyc: L1-L18, L1-L19, L3-L22, L49-L68
.agent/orchestrator/__pycache__/context_pruner.cpython-312.pyc: L10-L29, L21-L40, L35-L54, L34-L53, L65-L77
.agent/orchestrator/__pycache__/context_pruner.cpython-314.pyc: L39-L58, L15-L34, L25-L44, L1-L16, L59-L78
.agent/orchestrator/__pycache__/copyright_guard.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/copyright_guard.cpython-314.pyc: L1-L20
.agent/orchestrator/__pycache__/file_writer.cpython-312.pyc: L8-L27, L32-L51, L15-L34, L1-L20, L17-L36
.agent/orchestrator/__pycache__/file_writer.cpython-314.pyc: L31-L50, L3-L22, L1-L20, L17-L36, L2-L21
.agent/orchestrator/__pycache__/graph.cpython-312.pyc: L9-L23, L1-L20, L4-L23, L1-L19, L6-L23
.agent/orchestrator/__pycache__/graph.cpython-314.pyc: L10-L29, L24-L37, L13-L32, L7-L26, L15-L34
.agent/orchestrator/__pycache__/hooks.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/hooks.cpython-314.pyc: L1-L16
.agent/orchestrator/__pycache__/kobold_client.cpython-312.pyc: L1-L17, L1-L19
.agent/orchestrator/__pycache__/kobold_client.cpython-314.pyc: L1-L18, L1-L20, L2-L21
.agent/orchestrator/__pycache__/page_extractor.cpython-312.pyc: L36-L55, L34-L53, L1-L20, L2-L21
.agent/orchestrator/__pycache__/page_extractor.cpython-314.pyc: L34-L53, L1-L19, L32-L51
.agent/orchestrator/__pycache__/patch_applier.cpython-312.pyc: L26-L45, L55-L60, L1-L17, L7-L26, L4-L23
.agent/orchestrator/__pycache__/patch_applier.cpython-314.pyc: L63-L68, L24-L43, L1-L20, L4-L23, L1-L19
.agent/orchestrator/__pycache__/playwright_research.cpython-312.pyc: L14-L33, L1-L18, L1-L19
.agent/orchestrator/__pycache__/playwright_research.cpython-314.pyc: L14-L33, L1-L20, L1-L19
.agent/orchestrator/__pycache__/prompt_compiler.cpython-312.pyc: L10-L29, L14-L33, L1-L19, L11-L30, L1-L18
.agent/orchestrator/__pycache__/prompt_compiler.cpython-314.pyc: L39-L58, L26-L45, L31-L50, L24-L43, L12-L31
.agent/orchestrator/__pycache__/research_client.cpython-312.pyc: L66-L82, L45-L64, L13-L32, L1-L19, L16-L35
.agent/orchestrator/__pycache__/research_client.cpython-314.pyc: L20-L39, L170-L189, L78-L97, L9-L28, L80-L99
.agent/orchestrator/__pycache__/response_parser.cpython-312.pyc: L1-L17, L16-L35
.agent/orchestrator/__pycache__/response_parser.cpython-314.pyc: L93-L112, L98-L117, L90-L109, L96-L115, L1-L16
.agent/orchestrator/__pycache__/retry_engine.cpython-312.pyc: L1-L17
.agent/orchestrator/__pycache__/retry_engine.cpython-314.pyc: L83-L102, L72-L91, L70-L89, L74-L93, L103-L122
.agent/orchestrator/__pycache__/role_loader.cpython-312.pyc: L3-L22, L4-L23, L9-L28, L6-L25, L8-L27
.agent/orchestrator/__pycache__/role_loader.cpython-314.pyc: L7-L26, L6-L25, L4-L23
.agent/orchestrator/__pycache__/safety_guard.cpython-312.pyc: L39-L55, L24-L43, L4-L23, L22-L41, L1-L19
.agent/orchestrator/__pycache__/safety_guard.cpython-314.pyc: L26-L45, L20-L39, L21-L40, L38-L54, L27-L46
.agent/orchestrator/__pycache__/search_result_parser.cpython-312.pyc: L1-L17, L19-L38, L12-L31
.agent/orchestrator/__pycache__/search_result_parser.cpython-314.pyc: L1-L16, L22-L41, L11-L30
.agent/orchestrator/__pycache__/session_router.cpython-312.pyc: L31-L50, L10-L29, L4-L23, L36-L55, L30-L49
.agent/orchestrator/__pycache__/session_router.cpython-314.pyc: L20-L39, L23-L42, L3-L22, L24-L43, L22-L41
.agent/orchestrator/__pycache__/skill_registry.cpython-312.pyc: L54-L61, L24-L43, L12-L31, L7-L26, L22-L41
.agent/orchestrator/__pycache__/skill_registry.cpython-314.pyc: L10-L29, L20-L39, L23-L42, L3-L22, L48-L58
.agent/orchestrator/__pycache__/source_indexer.cpython-312.pyc: L10-L29, L23-L42, L1-L20, L1-L19, L1-L18
.agent/orchestrator/__pycache__/source_indexer.cpython-314.pyc: L10-L29, L20-L39, L1-L17, L1-L19, L1-L18
.agent/orchestrator/__pycache__/source_summarizer.cpython-312.pyc: L1-L7
.agent/orchestrator/__pycache__/state_store.cpython-312.pyc: L116-L135, L35-L54, L97-L116, L108-L127, L96-L115
.agent/orchestrator/__pycache__/state_store.cpython-314.pyc: L118-L137, L4-L23, L112-L131, L99-L118, L30-L49
.agent/orchestrator/__pycache__/studio_loop.cpython-312.pyc: L50-L69, L23-L42, L176-L195, L22-L41, L183-L202
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc: L335-L354, L161-L180, L20-L39, L23-L42, L170-L189
.agent/orchestrator/__pycache__/studio_loop.cpython-314.pyc.3098252610704: L23-L42, L170-L189, L103-L122, L22-L41, L167-L186
.agent/orchestrator/__pycache__/test_runner.cpython-312.pyc: L1-L18
.agent/orchestrator/__pycache__/test_runner.cpython-314.pyc: L1-L18
.agent/orchestrator/__pycache__/transition_engine.cpython-312.pyc: L1-L17, L7-L26, L12-L31, L13-L32
.agent/orchestrator/__pycache__/transition_engine.cpython-314.pyc: L9-L28, L10-L29, L1-L16, L2-L21
.agent/orchestrator/__pycache__/web_fetcher.cpython-312.pyc: L1-L19
.agent/orchestrator/__pycache__/web_research.cpython-312.pyc: L1-L17
.agent/skills/asset_creator_skills.md: L33-L43, L29-L43
.agent/skills/designer_skills.md: L49-L60, L51-L60, L15-L34, L22-L41, L25-L44
.agent/skills/developer_skills.md: L48-L63, L1-L16, L1-L15, L57-L63, L52-L63
.agent/skills/producer_skills.md: L27-L46, L9-L28, L41-L48, L43-L48
.agent/skills/qa_skills.md: L26-L45, L21-L40, L37-L48, L22-L41, L16-L35
.agent/skills/registry.json: L2-L13, L1-L13, L4-L13, L6-L13, L3-L13
.agent/skills/researcher_skills.md: L10-L29, L87-L97, L35-L54, L1-L20, L58-L77
.agent/skills/asset_creator/skill.json: L4-L15, L2-L15, L1-L15
.agent/skills/asset_creator/SKILL.md: L1-L3
.agent/skills/bug_hunter/skill.json: L1-L17, L6-L20, L1-L16, L2-L20
.agent/skills/bug_hunter/SKILL.md: L1-L3
.agent/skills/debug_dev/skill.json: L9-L15, L2-L15, L4-L15, L1-L15, L7-L15
.agent/skills/debug_dev/SKILL.md: L1-L3
.agent/skills/designer/skill.json: L1-L17, L6-L20, L1-L16, L2-L20
.agent/skills/designer/SKILL.md: L1-L3
.agent/skills/developer/skill.json: L9-L15, L2-L15, L4-L15, L1-L15, L7-L15
.agent/skills/developer/SKILL.md: L1-L3
.agent/skills/producer/skill.json: L1-L17, L6-L20, L1-L16, L2-L20
.agent/skills/producer/SKILL.md: L1-L3
.agent/skills/qa/skill.json: L1-L17, L6-L20, L1-L16, L2-L20
.agent/skills/qa/SKILL.md: L1-L3
.agent/skills/researcher/skill.json: L1-L17, L8-L21, L1-L19, L2-L21, L15-L21
.agent/skills/researcher/SKILL.md: L1-L3
.agent/workflows/asset_creator.md: L35-L42, L3-L22, L24-L42, L19-L38, L16-L35
.agent/workflows/bug_hunter.md: L4-L23, L21-L40, L17-L36, L33-L40
.agent/workflows/concept_producer.md: L4-L23, L32-L51, L33-L51, L44-L51
.agent/workflows/debug_dev.md: L34-L41, L4-L23, L1-L19, L11-L30
.agent/workflows/designer.md: L23-L42, L24-L43, L3-L22, L36-L43, L28-L43
.agent/workflows/developer.md: L10-L29, L20-L39, L49-L63, L12-L31, L3-L22
.agent/workflows/qa_tester.md: L20-L39, L21-L40, L3-L22, L14-L33, L25-L44
.agent/workflows/researcher.md: L39-L58, L26-L45, L10-L29, L54-L61, L12-L31
.agent/workflows/STUDIO_LOOP_WORKFLOW.md: L78-L96, L23-L42, L1-L20, L1-L18, L8-L27
.agent/workflows/task_template.md: L10-L29, L21-L40, L47-L54, L12-L31, L13-L32
docs/local_setup.md: L10-L29, L58-L63, L1-L17, L50-L63, L2-L21
docs/verification/browser_research_mdn_requestanimationframe.md: L31-L50, L12-L31, L13-L32, L46-L53, L14-L33
tests/e2e_loop_test.py: L13-L32, L67-L86, L97-L116, L22-L41, L11-L30
tests/real_browser_research_check.py: L32-L51, L3-L22, L35-L54, L34-L53, L41-L60
tests/regression_page_extractor.py: L18-L30, L1-L18, L5-L24
tests/test_autonomous_loop.py: L10-L29, L50-L69, L67-L86, L57-L76, L49-L68
tests/test_browser_research_mock.py: L128-L147, L13-L32, L103-L122, L67-L86, L166-L185
tests/test_gemma4_factory_tuning.py: L1-L20, L35-L51, L11-L30
tests/test_kobold_client.py: L4-L23, L23-L42, L11-L30
tests/test_local_codebase_audit.py: L350-L369, L397-L416, L411-L430, L285-L304, L420-L439
tests/test_repair_prompt.py: L128-L147, L13-L32, L103-L122, L215-L234, L114-L133
tests/test_response_parser.py: L237-L256, L10-L29, L20-L39, L301-L320, L358-L377
tests/test_robustness.py: L13-L32, L34-L53, L91-L105, L78-L97, L32-L51
tests/test_sessions_and_skills.py: L170-L189, L103-L122, L67-L86, L166-L185, L22-L41
tests/fixtures/research_mdn_requestanimationframe.json: L1-L16, L15-L24, L3-L22, L9-L24
tests/__pycache__/test_browser_research_mock.cpython-314.pyc: L23-L42, L24-L43, L27-L46, L74-L93, L75-L94
tests/__pycache__/test_repair_prompt.cpython-314.pyc: L103-L122, L22-L41, L123-L142, L167-L186, L174-L193
tests/__pycache__/test_response_parser.cpython-314.pyc: L31-L50, L23-L42, L63-L82, L11-L30, L96-L115
tests/__pycache__/test_robustness.cpython-314.pyc: L10-L29, L65-L82, L3-L22, L62-L81, L14-L33
tools/bootstrap_local_env.py: L48-L67, L97-L116, L78-L97, L47-L66
tools/bundle_project.py: L50-L69, L34-L53, L67-L86, L57-L76, L89-L108
tools/check_perms.py: L3-L22, L1-L20, L2-L21, L7-L25, L1-L18
tools/context_culler.py: L50-L69, L13-L32, L34-L53, L11-L30, L9-L28
tools/find_bloat.py: L33-L45, L23-L42, L1-L17, L1-L20, L19-L38
tools/test_orchestrator.py: L116-L135, L20-L39, L96-L115, L92-L111, L104-L123
tools/verify_clean_runtime.py: L128-L147, L218-L237, L10-L29, L176-L195, L261-L280
tools/__pycache__/verify_clean_runtime.cpython-314.pyc: L39-L58, L10-L29, L20-L39, L3-L22, L62-L81
tools/__pycache__/__init__.cpython-314.pyc: L1-L2

