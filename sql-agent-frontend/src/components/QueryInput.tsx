import { useState, type KeyboardEvent } from 'react'	 
interface Props {
onSubmit: (question:string) => void 
loading:boolean}

export function QueryInput({ onSubmit, loading }: Props) { 
    const[input, setInput] = useState('')

    function	handleSubmit()	{	
    if (!input.trim() || loading)  return
    onSubmit(input.trim()) 
    setInput('')
    }

    function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>){
    if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
         e.preventDefault() 
         handleSubmit()
        }
    }

    return(
    <div className="query-input"> 
        <textarea
            value={input}
            onChange={e => setInput(e.target.value)} 
            onKeyDown={handleKeyDown}
            placeholder="Use natural language(English) to ask, like which area has the highest sales?"
            disabled={loading} 
            rows={5}
        />
        <button onClick={handleSubmit} disabled={loading || !input.trim()}>	
        {loading? 'Analysizing...':'Ask'}
        </button>
    </div>
    )
}