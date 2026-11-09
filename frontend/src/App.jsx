import React, { useState, useEffect, useRef } from 'react';
import ChatHeader from './components/ChatHeader';
import ChatMessage from './components/ChatMessage';
import TypingIndicator from './components/TypingIndicator';
import MessageInput from './components/MessageInput';
import QuickMenu from './components/QuickMenu';
import DatasetModal from './components/DatasetModal';
import ProfileModal from './components/ProfileModal';
import { api } from './api/client';

const INITIAL_WELCOME = `Hello! 👋 Welcome to Student Academic Assistant.

I'm your personal academic assistant. I can help you understand your attendance, internal examination performance and academic progress.

To get started, please enter your Student ID.`;

export default function App() {
  const [messages, setMessages] = useState([]);
  const [sessionToken, setSessionToken] = useState(null);
  const [studentId, setStudentId] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isDatasetModalOpen, setIsDatasetModalOpen] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Set initial welcome message on mount
  useEffect(() => {
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages([
      {
        id: 'msg-welcome',
        sender: 'bot',
        text: INITIAL_WELCOME,
        timestamp: now,
        buttons: [],
        card_type: null,
        card_data: null,
      },
    ]);
  }, []);

  // Handle sending a message
  const handleSendMessage = async (textToSend, customDisplayLabel = null) => {
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // 1. Append user message to chat
    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: customDisplayLabel || textToSend,
      timestamp: now,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      // 2. Send to Flask backend
      const response = await api.sendChat(textToSend, sessionToken);

      const botTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      // Update session state if returned
      if (response.session_token && !sessionToken) {
        setSessionToken(response.session_token);
        setStudentId(response.student_id);
        setIsAuthenticated(true);
      } else if (!response.is_authenticated && sessionToken) {
        // User logged out
        setSessionToken(null);
        setStudentId(null);
        setIsAuthenticated(false);
      }

      // 3. Append bot response
      const botMsg = {
        id: `bot-${Date.now()}`,
        sender: 'bot',
        text: response.text,
        timestamp: botTime,
        buttons: response.buttons || [],
        card_type: response.card_type,
        card_data: response.card_data,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error('Chat error:', err);
      const botTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages((prev) => [
        ...prev,
        {
          id: `bot-err-${Date.now()}`,
          sender: 'bot',
          text: `⚠️ *Communication Error*\n\n${err.message || 'Unable to connect to the Flask server. Please make sure the backend is running.'}`,
          timestamp: botTime,
          buttons: [],
          card_type: null,
          card_data: null,
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  // Handle clicking quick menu buttons
  const handleMenuOptionSelect = (command, label) => {
    handleSendMessage(command, label);
  };

  // Quick select sample student ID
  const handleQuickStudentSelect = (id) => {
    handleSendMessage(id);
  };

  // Handle logout
  const handleLogout = async () => {
    if (sessionToken) {
      try {
        await api.logout(sessionToken);
      } catch (e) {
        // ignore logout network errors
      }
    }
    setSessionToken(null);
    setStudentId(null);
    setIsAuthenticated(false);

    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages((prev) => [
      ...prev,
      {
        id: `logout-${Date.now()}`,
        sender: 'bot',
        text: `🔒 *Session Ended*\n\nYou have been logged out. To view another student's academic progress, please enter the new Student ID.`,
        timestamp: now,
        buttons: [],
        card_type: null,
        card_data: null,
      },
    ]);
  };

  return (
    <div className="flex h-screen w-screen bg-[#0b141a] sm:p-3 md:p-5 items-center justify-center font-['Segoe_UI',Helvetica,Arial,sans-serif]">
      {/* WhatsApp Window Container */}
      <div className="flex flex-col h-full w-full max-w-4xl bg-white sm:rounded-2xl shadow-2xl overflow-hidden border border-gray-800/20 relative">
        {/* Top Header */}
        <ChatHeader
          studentId={studentId}
          isAuthenticated={isAuthenticated}
          isTyping={isTyping}
          onLogout={handleLogout}
          onOpenDatasetModal={() => setIsDatasetModalOpen(true)}
          onOpenProfile={() => setIsProfileModalOpen(true)}
        />

        {/* WhatsApp Chat Area */}
        <div className="flex-1 overflow-y-auto px-4 py-4 bg-whatsapp-chatBg bg-whatsapp-pattern relative space-y-1">
          {/* WhatsApp Security Encryption Banner */}
          <div className="flex justify-center mb-3">
            <div className="bg-[#ffeecd] text-[#54656f] text-[11px] font-medium px-3.5 py-1.5 rounded-lg shadow-2xs max-w-md text-center leading-tight border border-[#ffd279]/50">
              🔒 <span className="font-semibold">Rule-Based Academic Session.</span> Individual student records are verified and evaluated directly using Python logic on the Flask backend. Zero LLM hallucinations.
            </div>
          </div>

          {/* Messages list */}
          {messages.map((msg) => (
            <ChatMessage
              key={msg.id}
              message={msg}
              onButtonClick={handleMenuOptionSelect}
            />
          ))}

          {/* Interactive Menu pills if authenticated */}
          {isAuthenticated && !isTyping && (
            <div className="max-w-[90%] sm:max-w-[80%] md:max-w-[70%] mb-3">
              <QuickMenu onSelectOption={handleMenuOptionSelect} disabled={isTyping} />
            </div>
          )}

          {/* Typing Indicator */}
          {isTyping && <TypingIndicator />}

          {/* Scroll anchor */}
          <div ref={messagesEndRef} />
        </div>

        {/* Bottom Message Input Bar */}
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={isTyping}
          isAuthenticated={isAuthenticated}
          onQuickStudentSelect={handleQuickStudentSelect}
        />
      </div>

      {/* Dataset Info Modal */}
      <DatasetModal
        isOpen={isDatasetModalOpen}
        onClose={() => setIsDatasetModalOpen(false)}
      />

      {/* Student Profile Modal */}
      <ProfileModal
        isOpen={isProfileModalOpen}
        onClose={() => setIsProfileModalOpen(false)}
        sessionToken={sessionToken}
        onLogout={handleLogout}
        onSelectOption={handleMenuOptionSelect}
      />
    </div>
  );
}

