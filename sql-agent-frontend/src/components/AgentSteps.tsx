import type { Step } from '../types/agent';

const TOOL_LABELS: Record<string, string> = {
  list_tables: '查看所有表',
  describe_table: '查看表结构',
  execute_sql: '执行 SQL',
};

export function AgentSteps({ steps }: { steps: Step[] }) {
  if (steps.length === 0) return null;
  
  return (
    <div className="agent-steps">
      <p className="steps-title">Agent 执行步骤</p>
      {steps.map((step, i) => (
        <div key={i} className="step">
          <span className="step-label">{TOOL_LABELS[step.tool] ?? step.tool}</span>
          {step.tool === 'execute_sql' && (
            <pre className="sql-code">{step.input.query}</pre>
          )}
          {step.tool === 'describe_table' && (
            <span className="step-detail">表: {step.input.table_name}</span>
          )}
        </div>
      ))}
    </div>
  );
}