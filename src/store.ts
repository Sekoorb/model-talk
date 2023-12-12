import { create } from 'zustand';

const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api`
  : 'http://localhost:8000/api';

type Chat = {
  id: number;
  prompt: string;
  reply: string;
};

type CreateChat = {
  prompt: string;
};

type ChatStore = {
  chats: Chat[];
  fetchChats: () => Promise<void>;
  addChat: (chat: CreateChat) => Promise<void>;
};

export const useStore = create<ChatStore>((set, get) => ({
  chats: [],
  fetchChats: async () => {
    try {
      const response = await fetch(`${URL}/chats`);
      const chats = await response.json();
      set({ chats });
    } catch (error) {
      console.error('Error fetching chats:', error);
    }
  },
// In store.ts
addChat: async (chat: CreateChat) => {
  try {
    const id = get().chats.length + 1; // Store the ID here to use later
    set((state) => ({ chats: [...state.chats, { ...chat, id: id, reply: '' }] }));
    
    const eventSource = new EventSource(`${URL}/stream?prompt=${encodeURIComponent(chat.prompt)}`);
    
    eventSource.onmessage = (event) => {
      const data = event.data;
      set((state) => {
        const chats = state.chats.map((c) => {
          if (c.id === id) {
            return { ...c, reply: c.reply + data };
          }
          return c;
        });
        return { chats };
      });
    };

    eventSource.addEventListener('end-of-stream', () => {
      console.log('Chat stream ended normally.');
      eventSource.close();
      set((state) => {
        const chats = state.chats.map((c) => {
          if (c.id === id) {
            return { ...c, reply: c.reply.trim() }; // Trim any possible trailing newlines
          }
          return c;
        });
        return { chats };
      });
    });

    eventSource.onerror = (error) => {
      if (eventSource.readyState === EventSource.CLOSED) {
        console.log('Chat stream ended normally.');
      } else {
        console.error('Error with the chat stream:', error);
      }
      eventSource.close();
    };

  } catch (error) {
    console.error('Error adding chat:', error);
  }
},
}));
