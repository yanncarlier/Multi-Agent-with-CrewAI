## Purpose of modular_versions

The modular versions are designed to be more flexible and maintainable alternatives to monolithic scripts. They separate configuration from code by:

1. **Loading agent and task definitions from markdown files** instead of hardcoding them
2. **Making workflows easily configurable** without modifying Python code
3. **Providing cleaner separation of concerns** between logic and prompts

## Current modular workflows

- **content_creation**: YouTube Shorts content planning workflow
- **automatic_deep_research**: Multi-agent research workflow with web scraping
- **agents_automatic_code_review**: 3-agent code review system (Senior Developer → Security Engineer → Tech Lead)

## Key benefits

- **Easier customization**: Modify agent prompts by editing markdown files
- **Better maintainability**: Configuration changes don't require code changes
- **Reusability**: Same workflow can be used with different configurations
- **Clarity**: Separates what the agents do (prompts) from how they work (code)