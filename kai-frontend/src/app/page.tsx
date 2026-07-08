'use client';
import { useEffect, useState } from 'react';
import { LiveKitRoom, RoomAudioRenderer, StartAudio, DisconnectButton } from '@livekit/components-react';
import { KaiAvatar } from '../components/KaiAvatar';
import { ChatInput } from '../components/ChatInput';

export default function Home() {
  const [tokenData, setTokenData] = useState<{token: string, url: string} | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/get-token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ room_name: "avatar-room", participant_name: "Roschlynn" }),
    })
      .then((res) => res.json())
      .then(setTokenData);
  }, []);

  if (!tokenData) return <div className="text-white flex items-center justify-center h-screen">Connecting...</div>;

  return (
    <LiveKitRoom 
      serverUrl={tokenData.url} 
      token={tokenData.token} 
      connect={true}
      className="h-screen w-screen relative overflow-hidden" 
    >
      <RoomAudioRenderer />
      <div className="absolute top-6 right-6">
        <DisconnectButton className="bg-red-600/20 text-red-500 border border-red-500/50 px-4 py-2 rounded-xl hover:bg-red-600 hover:text-white transition">
          End Session
        </DisconnectButton>
      </div>

      <div className="absolute inset-0 z-50 flex items-center justify-center pointer-events-none">
        <StartAudio 
          label="Click to start conversation" 
          className="pointer-events-auto px-8 py-4 bg-white/10 backdrop-blur-md border border-white/20 text-white rounded-full font-semibold text-lg hover:bg-white/20 hover:scale-105 transition-all shadow-2xl" 
        />
      </div>
      <div className="absolute inset-0 z-0">
        <KaiAvatar/>
      </div>
      
      <div className="absolute bottom-0 left-0 w-full p-6 flex justify-center">
        <ChatInput />
      </div>
    </LiveKitRoom>
  );
}