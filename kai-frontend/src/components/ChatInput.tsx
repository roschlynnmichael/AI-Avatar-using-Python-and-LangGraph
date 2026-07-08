'use client';
import { useRoomContext } from '@livekit/components-react';
import { useState } from 'react';

export function ChatInput() {
  const room = useRoomContext();
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;

    const payload = JSON.stringify({ message: input });
    const encoder = new TextEncoder();

    room.localParticipant.publishData(encoder.encode(payload), { 
      reliable: true,
      topic: 'lk-chat-topic'
    });
    
    console.log("Sent to Liv:", input);
    setInput('');
  };

  return (
    <div className="w-full max-w-2xl bg-black/30 backdrop-blur-lg border border-white/10 rounded-3xl p-4 shadow-2xl flex items-center gap-3">
      <input 
        className="flex-1 bg-transparent p-2 text-white placeholder-gray-300 outline-none text-lg"
        placeholder="Talk to Kai..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            handleSend();
          }
        }}
      />
      <button 
        onClick={handleSend}
        className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-full transition-all"
      >
        Send
      </button>
    </div>
  );
}