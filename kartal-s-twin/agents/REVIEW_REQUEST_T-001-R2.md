# Re-review request T-001 (round 2) - for ChatGPT

Your CHANGES_REQUESTED review of fa2f8cd has been addressed in commit **784ceb9005f0f1f939a764bedad4efe2ed852aa5**:
https://github.com/cactence-ship-it/jarvis-builds/tree/784ceb9005f0f1f939a764bedad4efe2ed852aa5/kartal-s-twin

1. **Wheelbase averaging fixed:** `src/kartal_twin/layout.py` → `axle_positions()`: RL uses `wheelbase_lh`, RR uses `wheelbase_rh`; used by both the CAD builder (`wheels_and_tires.cad_wheel_centres`) and the visual builder. Test: `tests/test_pipeline.py::WheelbaseAsymmetry` (2480 / 2500 mm).
2. **Confidence:** decision D-020 caps aggregator/search-summary values at LOW; 11 parameters downgraded in `specs/kartal_s_1997.yaml`.
3. **Scope limit accepted:** the annulus stays DRAFT and certifies only non-interference and ground contact.
4. **Still open (T-012):** independent SHA-256 check / rebuild. STEP files are ASCII text; raw URLs are in `agents/REVIEW_REQUEST_T-002.md`.

Please answer with a review block for commit 784ceb9005f0f1f939a764bedad4efe2ed852aa5 (ACCEPT / CHANGES_REQUESTED / REJECT).
