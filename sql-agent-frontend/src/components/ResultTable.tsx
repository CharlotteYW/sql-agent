import type { Step } from '../types/agent';

export function ResultTable({ steps }: { steps: Step[] }) {
  // 找到 execute_sql 的结果
  const sqlStep = steps.findLast(s => s.tool === 'execute_sql');
  
  if (!sqlStep) return null;
  
  let rows: Record<string, unknown>[] = [];
  
  try {
    rows = JSON.parse(sqlStep.result);
  } catch {
    return null;
  }
  
  if (!rows || rows.length === 0) return <p className="no-data">查询结果为空</p>;
  
  const columns = Object.keys(rows[0]);
  
  return (
    <div className="result-table-wrapper">
      <p className="table-title">查询结果({rows.length}行)</p>
      <table className="result-table">
        <thead>
          <tr>
            {columns.map(col => <th key={col}>{col}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {columns.map(col => (
                <td key={col}>{String(row[col] ?? '')}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}