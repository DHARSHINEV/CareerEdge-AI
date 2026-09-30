"""
CareerEdge AI - 30-Day Personalized Career Upgrade Roadmap Generator
Synthesizes a structured, day-by-day plan linking every single action to
detected skill gaps from the job matching analysis.
"""

from typing import Dict, Any, List
from backend.models.schemas import (
    RoadmapResponse,
    RoadmapWeek,
    RoadmapDayTask,
    SkillMatchDetail,
)


class RoadmapGenerator:
    """
    Generates structured 30-day upgrade plans broken down into 4 coherent weekly milestones:
    Week 1: Fundamentals & Theory
    Week 2: Hands-On Architecture & Implementation
    Week 3: Deployment, Tooling & Optimization
    Week 4: Portfolio Packaging, Resume Integration & Interview Evidence
    """

    def generate_roadmap(
        self,
        target_role: str,
        critical_gaps: List[SkillMatchDetail],
    ) -> RoadmapResponse:
        # Identify target gap skills
        gap_skills = [g.requirement for g in critical_gaps]
        if not gap_skills:
            gap_skills = ["Docker", "PyTorch", "AWS"]

        primary_gap = gap_skills[0] if len(gap_skills) > 0 else "Advanced AI"
        secondary_gap = gap_skills[1] if len(gap_skills) > 1 else primary_gap
        tertiary_gap = gap_skills[2] if len(gap_skills) > 2 else secondary_gap

        # Week 1: Fundamentals & Environment Setup
        week1_tasks = [
            RoadmapDayTask(
                day=1,
                title=f"Core Foundations of {primary_gap}",
                description=f"Study core design patterns, runtime architecture, and standard documentation for {primary_gap}.",
                linked_gap=primary_gap,
                deliverable=f"Completed local cheat sheet and architecture diagram for {primary_gap}.",
            ),
            RoadmapDayTask(
                day=2,
                title=f"Hands-On Hello World with {primary_gap}",
                description=f"Initialize a clean development workspace and write first functional prototype using {primary_gap}.",
                linked_gap=primary_gap,
                deliverable=f"Git repository with tested standalone {primary_gap} script.",
            ),
            RoadmapDayTask(
                day=3,
                title=f"Fundamentals of {secondary_gap}",
                description=f"Understand how {secondary_gap} fits into modern production pipelines for {target_role}.",
                linked_gap=secondary_gap,
                deliverable=f"Summary notes on key commands and configuration syntax for {secondary_gap}.",
            ),
            RoadmapDayTask(
                day=4,
                title=f"Interactive Experimentation with {secondary_gap}",
                description=f"Build small proof-of-concept scripts combining {primary_gap} and {secondary_gap}.",
                linked_gap=secondary_gap,
                deliverable="Working integration script running without errors.",
            ),
            RoadmapDayTask(
                day=5,
                title=f"Exploration of {tertiary_gap}",
                description=f"Review foundational concepts, security boundaries, and API interfaces for {tertiary_gap}.",
                linked_gap=tertiary_gap,
                deliverable=f"Annotated configuration file for {tertiary_gap}.",
            ),
            RoadmapDayTask(
                day=6,
                title="Weekly Review & Concept Synthesis",
                description="Consolidate learnings across all three gap technologies and diagram the system architecture.",
                linked_gap="Cross-Discipline Synthesis",
                deliverable="System architecture diagram covering all 3 target skills.",
            ),
            RoadmapDayTask(
                day=7,
                title="Rest & Project Planning",
                description="Draft the technical specification for next week's capstone project.",
                linked_gap="Project Planning",
                deliverable="1-page project README and schema draft.",
            ),
        ]

        # Week 2: Hands-On Project Implementation
        week2_tasks = [
            RoadmapDayTask(
                day=8,
                title="Initialize Capstone Project Structure",
                description=f"Set up modular project repository, virtual environment, and dependency tracking for {primary_gap}.",
                linked_gap=primary_gap,
                deliverable="Clean repository initialized with README and dependency lockfile.",
            ),
            RoadmapDayTask(
                day=9,
                title=f"Build Data/Inference Pipeline with {primary_gap}",
                description=f"Implement core processing logic, error handling, and unit test fixtures with {primary_gap}.",
                linked_gap=primary_gap,
                deliverable="Automated unit tests passing for pipeline module.",
            ),
            RoadmapDayTask(
                day=10,
                title=f"Integrate {secondary_gap} Service Layer",
                description=f"Expose pipeline via REST API endpoints or containerized interface using {secondary_gap}.",
                linked_gap=secondary_gap,
                deliverable="Documented API endpoints or runnable interface.",
            ),
            RoadmapDayTask(
                day=11,
                title="Add Data Validation & Schema Enforcement",
                description="Implement strict input/output validation, error responses, and configuration management.",
                linked_gap="Software Engineering Rigor",
                deliverable="Pydantic models and input validation tests.",
            ),
            RoadmapDayTask(
                day=12,
                title=f"Connect {tertiary_gap} Integration",
                description=f"Wire up {tertiary_gap} for storage, logging, telemetry, or cloud execution.",
                linked_gap=tertiary_gap,
                deliverable=f"End-to-end data flow verified with {tertiary_gap}.",
            ),
            RoadmapDayTask(
                day=13,
                title="Integration Testing & Edge Case Hardening",
                description="Simulate network drops, malformed payloads, and edge case failure modes.",
                linked_gap="System Resilience",
                deliverable="Integration test suite with coverage report.",
            ),
            RoadmapDayTask(
                day=14,
                title="Code Refactoring & Clean Architecture Review",
                description="Clean up modular imports, add docstrings, and run linters.",
                linked_gap="Code Quality",
                deliverable="Zero lint errors and modular code organization.",
            ),
        ]

        # Week 3: Deployment, Tooling & Optimization
        week3_tasks = [
            RoadmapDayTask(
                day=15,
                title=f"Containerize Application with {secondary_gap}",
                description=f"Write optimized multi-stage Dockerfile or container spec for the application.",
                linked_gap=secondary_gap,
                deliverable="Minimal, reproducible container image built locally.",
            ),
            RoadmapDayTask(
                day=16,
                title="Local Container Verification & Health Checks",
                description="Configure container health checks, environment secrets, and port forwarding.",
                linked_gap=secondary_gap,
                deliverable="Healthy container execution verified via curl / HTTP tests.",
            ),
            RoadmapDayTask(
                day=17,
                title=f"Performance Benchmarking of {primary_gap}",
                description="Measure execution latency, P95 metrics, memory consumption, and throughput.",
                linked_gap=primary_gap,
                deliverable="Benchmark summary table with cold vs warm run times.",
            ),
            RoadmapDayTask(
                day=18,
                title="Inference Optimization / Quantization",
                description="Apply ONNX export, INT8/FP16 quantization, or caching to cut compute overhead.",
                linked_gap="Optimization & Efficiency",
                deliverable="Quantized model/binary demonstrating measurable speedup.",
            ),
            RoadmapDayTask(
                day=19,
                title="Set Up Automated CI/CD Pipeline",
                description="Create GitHub Actions workflow running tests and linter automatically on push.",
                linked_gap="DevOps & Automation",
                deliverable="Passing green CI build badge in repository.",
            ),
            RoadmapDayTask(
                day=20,
                title=f"Deploy to Staging / {tertiary_gap}",
                description=f"Deploy service to cloud staging or local sandbox environment using {tertiary_gap}.",
                linked_gap=tertiary_gap,
                deliverable="Live URL or verified local production run script.",
            ),
            RoadmapDayTask(
                day=21,
                title="Write Comprehensive Technical Documentation",
                description="Document architecture diagram, installation steps, and API contract in README.",
                linked_gap="Technical Communication",
                deliverable="Polished GitHub README with screenshots and curl examples.",
            ),
        ]

        # Week 4: Portfolio Packaging & Resume Evidence
        week4_tasks = [
            RoadmapDayTask(
                day=22,
                title="Record 2-Minute Video Demo / GIF Walkthrough",
                description="Record a concise, professional screen recording showcasing the working system.",
                linked_gap="Demonstration Artifact",
                deliverable="Demo video or high-res GIF linked in README.",
            ),
            RoadmapDayTask(
                day=23,
                title=f"Synthesize Resume Bullets for {primary_gap}",
                description=f"Draft action-oriented bullet points with exact metrics (e.g. latency, throughput).",
                linked_gap=primary_gap,
                deliverable="2 quantified resume bullet points for experience section.",
            ),
            RoadmapDayTask(
                day=24,
                title=f"Synthesize Resume Bullets for {secondary_gap} & {tertiary_gap}",
                description="Draft project description bullet points emphasizing containerization and deployment.",
                linked_gap=secondary_gap,
                deliverable="Complete 3-bullet project entry ready for resume.",
            ),
            RoadmapDayTask(
                day=25,
                title="Update Online Portfolio & GitHub Profile",
                description="Pin repository to GitHub profile and update LinkedIn project showcase.",
                linked_gap="Public Visibility",
                deliverable="Public repository live with tags and topics.",
            ),
            RoadmapDayTask(
                day=26,
                title=f"Technical Interview Drill: {primary_gap} System Design",
                description=f"Prepare explanations for trade-offs, architecture decisions, and bottlenecks in {primary_gap}.",
                linked_gap=primary_gap,
                deliverable="Prepared answers for top 5 interview questions on this stack.",
            ),
            RoadmapDayTask(
                day=27,
                title="Mock Interview Walkthrough",
                description="Practice explaining the project from problem statement to measurable business impact in 3 minutes.",
                linked_gap="Interview Readiness",
                deliverable="Fluent 180-second elevator pitch recorded.",
            ),
            RoadmapDayTask(
                day=28,
                title="Run CareerEdge AI Re-Analysis",
                description="Upload updated resume draft to CareerEdge AI and verify alignment score increase.",
                linked_gap="Validation",
                deliverable="Re-analyzed profile showing converted strong matches.",
            ),
            RoadmapDayTask(
                day=29,
                title="Targeted Job Application Strategy",
                description="Shortlist 5 target roles that match the newly acquired qualifications.",
                linked_gap="Career Execution",
                deliverable="Curated spreadsheet of 5 target companies and roles.",
            ),
            RoadmapDayTask(
                day=30,
                title="30-Day Milestone Review & Submission",
                description="Celebrate completed project, validated competencies, and submit updated applications.",
                linked_gap="Milestone Completion",
                deliverable="Fully transformed, evidence-backed career profile.",
            ),
        ]

        weeks = [
            RoadmapWeek(
                week_number=1,
                theme="Fundamentals & Architectural Scaffolding",
                objective=f"Master foundational concepts and establish local development environments for {primary_gap}, {secondary_gap}, and {tertiary_gap}.",
                tasks=week1_tasks,
            ),
            RoadmapWeek(
                week_number=2,
                theme="Hands-On Capstone Project Implementation",
                objective=f"Build an end-to-end application integrating {primary_gap} and {secondary_gap} with automated testing.",
                tasks=week2_tasks,
            ),
            RoadmapWeek(
                week_number=3,
                theme="Containerization, Deployment & Benchmarking",
                objective="Package with Docker, measure execution latency, implement CI/CD, and optimize performance.",
                tasks=week3_tasks,
            ),
            RoadmapWeek(
                week_number=4,
                theme="Portfolio Packaging, Resume Evidence & Interview Readiness",
                objective="Add verified project evidence to resume, record demo, and rehearse technical system design drills.",
                tasks=week4_tasks,
            ),
        ]

        return RoadmapResponse(
            target_role=target_role,
            weeks=weeks,
            estimated_weekly_hours=10,
            total_duration_days=30,
        )


# Singleton instance
_roadmap_generator = None


def get_roadmap_generator() -> RoadmapGenerator:
    global _roadmap_generator
    if _roadmap_generator is None:
        _roadmap_generator = RoadmapGenerator()
    return _roadmap_generator
