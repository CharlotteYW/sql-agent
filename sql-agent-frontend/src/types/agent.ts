export interface Step{
    tool: string
    input: Record<string, string>
    result: string
}

export interface AgentResponse{
    steps: Step[]
    answer: string
}