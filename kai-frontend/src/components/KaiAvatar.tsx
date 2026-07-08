'use client';
import { useTracks, VideoTrack } from '@livekit/components-react';
import { Track } from 'livekit-client';

export function KaiAvatar() {
  const tracks = useTracks([Track.Source.Camera]);
  
  return (
    <div className="absolute inset-0 z-0 overflow-hidden bg-gray-900">
      {tracks.length > 0 ? (
        <VideoTrack 
          trackRef={tracks[0]} 
          className="w-full h-full object-cover transform scale-90 origin-center" 
        />
      ) : (
        <div className="flex items-center justify-center h-full text-white">
          Initializing Kai...
        </div>
      )}
    </div>
  );
}