import { ref } from 'vue'
import { defineStore } from 'pinia'
import { StreamVideoClient } from '@stream-io/video-client'
import type { Call, StreamVideoParticipant } from '@stream-io/video-client'
import type { Subscription } from 'rxjs'
import { useUserStore } from '@/stores/authStore'
import { StreamChat } from 'stream-chat';
import authAxios from '@/services/api/setup';

const baseURL = import.meta.env.VITE_API_URL;

export const useStreamStore = defineStore('stream', () => {
  const call = ref<Call>() // Holds the ref for the call
  const isBackstage = ref<boolean>(false) // Holds the boolean for backstage
  const isBackstageSub = ref<Subscription>() // holds the boolean for if user is backstage Sub
  const localParticipant = ref<StreamVideoParticipant>() // Holds the data for local stream participant 
  const localParticipantSub = ref<Subscription>() // Holds the data for local stream participant Subscriber
  const remoteParticipant = ref<StreamVideoParticipant>() // Holds the data for remote participant
  const remoteParticipantSub = ref<Subscription>() // Holds the data for remote particpant subscriber

  const streamVideoClientID = ref<string | null>(null);
  const streamVideoClientName = ref<string | null>(null);

  const apiKey = import.meta.env.VITE_STREAM_API_KEY;
  const apiSecret = import.meta.env.VITE_STREAM_API_SECRET;

  if (!apiKey) throw new Error('API key is not defined');

  let streamVideoClient = ref<StreamVideoClient>();

  async function loadUserData() {
    try {
      const userStore = useUserStore();
      await userStore.fetchUser();
  
      const user = userStore.user;
  
      if (!user || !user.user_ptr_id || !user.name) {
        throw new Error('User data is missing or incomplete');
      }
  
      streamVideoClientName.value = user.name;
      streamVideoClientID.value = user.user_ptr_id;
  
      const tokenProvider = async (id: string) => {
        try {
            const response = await authAxios.get(`${baseURL}/usermanagement/user/stream-token/${id}`);
            if (response.status !== 200) {
                throw new Error(`Failed to fetch token: ${response.statusText}`);
            }
            
            const token = response.data.token
            const user_id = response.data.user_id
            if (user_id !== id.toString()) {
                throw new Error("Mismatch between user ID and token user ID.");
            }
    
            return token; // Return only the token for the Stream client
        } catch (error) {
            console.error("Token fetch error:", error.message);
            throw error;
        }
      }

      const updatePermissionsForStream = async (id: string) => {
        try {
            const response = await authAxios.get(`${baseURL}/usermanagement/user/stream-admin/${id}`);
            if (response.status !== 200) {
                throw new Error(`Failed to fetch token: ${response.statusText}`);
            }
            
            return;
        } catch (error) {
            console.error("Token fetch error:", error.message);
            throw error;
        }
      }
  
      if (!streamVideoClientID.value || !streamVideoClientName.value) {
        throw new Error('User ID or name is missing');
      }

      let token = await tokenProvider(streamVideoClientID.value) as string;
      streamVideoClient.value = new StreamVideoClient({
        apiKey,
        token,
        user: {
          id: streamVideoClientID.value.toString(),
          name: streamVideoClientName.value,
          image: 'https://getstream.io/random_svg/?id=Snoke&name=Snoke',
        },
      });
      await updatePermissionsForStream(streamVideoClientID.value)
  
      console.log('StreamVideoClient initialized successfully');
    } catch (error) {
      console.error('Error loading user data or initializing StreamVideoClient:', error);
      throw error;
    }
  }

  function ensureClientInitialized() {
    if (!streamVideoClient) {
      throw new Error('StreamVideoClient is not initialized. Call loadUserData() first.');
    }
  }

  async function createCall(id: string) {
    ensureClientInitialized();
    try {
      const newCall = streamVideoClient.value!.call('livestream', id);
      await newCall.camera.enable();
      await newCall.microphone.enable();
      await newCall.join({ create: true });

      localParticipantSub.value = newCall.state.localParticipant$.subscribe(
        (updatedLocalParticipant) => {
          localParticipant.value = updatedLocalParticipant;
        }
      );

      isBackstageSub.value = newCall.state.backstage$.subscribe((backstage) => {
        isBackstage.value = backstage;
      });

      call.value = newCall;
    } catch (error) {
      console.error('Error creating call:', error);
      throw error;
    }
  }

  async function watchStream(id: string) {
    ensureClientInitialized();
    try {
      const newCall = streamVideoClient.value!.call('livestream', id);
      await newCall.camera.disable();
      await newCall.microphone.disable();
      await newCall.join();

      remoteParticipantSub.value = newCall.state.remoteParticipants$.subscribe(
        (newRemoteParticipants) => {
          remoteParticipant.value = newRemoteParticipants[0] || undefined;
        }
      );

      call.value = newCall;
    } catch (error) {
      console.error('Error watching stream:', error);
      throw error;
    }
  }

  async function endCall() {
    await call.value?.endCall();
    localParticipantSub.value?.unsubscribe();
    isBackstageSub.value?.unsubscribe();

    call.value = undefined;
  }

  async function leaveStream() {
    await call.value?.leave();
    remoteParticipantSub.value?.unsubscribe();

    call.value = undefined;
  }

  return {
    call,
    isBackstage,
    localParticipant,
    remoteParticipant,
    streamVideoClient,
    createCall,
    endCall,
    watchStream,
    leaveStream,
    loadUserData,
  };
});
