"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { useRouter } from "next/navigation";
import { useKindeBrowserClient } from "@kinde-oss/kinde-auth-nextjs";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

const validateGroqKey = (key: string) => {
  return key.startsWith('gsk_');
};

const validateAlpacaKey = (key: string) => {
  return /^[A-Z0-9]{20}$/.test(key);
};

const validateAlpacaSecret = (key: string) => {
  return /^[A-Za-z0-9]{40}$/.test(key);
};

export default function SettingsPage() {
  const router = useRouter();
  const { user, isLoading: isAuthLoading, getToken } = useKindeBrowserClient();
  const [isLoading, setIsLoading] = useState(false);
  const [keys, setKeys] = useState({
    groq: "",
    alpacaApiKey: "",
    alpacaSecretKey: "",
    alpacaEndpoint: "https://paper-api.alpaca.markets/v2",
  });

  const [errors, setErrors] = useState({
    groq: "",
    alpacaApiKey: "",
    alpacaSecretKey: "",
  });

  const [status, setStatus] = useState<{
    type: "success" | "error" | "";
    message: string;
  }>({ type: "", message: "" });

  const handleKeyChange = (keyType: string, value: string) => {
    setKeys((prev) => ({ ...prev, [keyType]: value }));
    
    // Validate on change
    switch (keyType) {
      case "groq":
        setErrors(prev => ({
          ...prev,
          groq: validateGroqKey(value) ? "" : "Invalid Groq key format. Should start with 'gsk_'"
        }));
        break;
      case "alpacaApiKey":
        setErrors(prev => ({
          ...prev,
          alpacaApiKey: validateAlpacaKey(value) ? "" : "Invalid Alpaca API key format. Should be 20 characters long"
        }));
        break;
      case "alpacaSecretKey":
        setErrors(prev => ({
          ...prev,
          alpacaSecretKey: validateAlpacaSecret(value) ? "" : "Invalid Alpaca secret key format. Should be 40 characters long"
        }));
        break;
    }
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      const token = await getToken();
      const response = await fetch("http://localhost:8000/api/v1/settings/keys", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(keys),
      });

      const data = await response.json();
      if (response.ok) {
        setStatus({ type: "success", message: "API keys saved successfully" });
      } else {
        setStatus({ 
          type: "error", 
          message: data.error || "Failed to save API keys" 
        });
      }
    } catch (error) {
      setStatus({ 
        type: "error", 
        message: "Unable to connect to the server" 
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isAuthLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-yellow-500" />
      </div>
    );
  }

  if (!user) {
    router.push("/");
    return null;
  }

  return (
    <div className="container mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-white mb-8">API Settings</h1>

      {status.message && (
        <div className={`p-4 rounded-lg mb-4 ${
          status.type === "success" ? "bg-green-500/20 text-green-200" : "bg-red-500/20 text-red-200"
        }`}>
          {status.message}
        </div>
      )}

      {/* LLM Section */}
      <div className="bg-black/50 p-6 rounded-lg border border-yellow-500/20">
        <h2 className="text-xl font-semibold text-white mb-4">LLM Configuration</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Groq API Key
            </label>
            <Input
              type="password"
              placeholder="gsk_..."
              value={keys.groq}
              onChange={(e) => handleKeyChange("groq", e.target.value)}
              className={`bg-black/30 border-yellow-500/30 text-white ${errors.groq ? "border-red-500" : ""}`}
              disabled={isLoading}
            />
            {errors.groq && (
              <p className="mt-1 text-sm text-red-500">{errors.groq}</p>
            )}
          </div>
        </div>
      </div>

      {/* Trading Section */}
      <div className="bg-black/50 p-6 rounded-lg border border-yellow-500/20">
        <h2 className="text-xl font-semibold text-white mb-4">Trading Configuration</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Alpaca API Key
            </label>
            <Input
              type="password"
              placeholder="PK..."
              value={keys.alpacaApiKey}
              onChange={(e) => handleKeyChange("alpacaApiKey", e.target.value)}
              className={`bg-black/30 border-yellow-500/30 text-white ${errors.alpacaApiKey ? "border-red-500" : ""}`}
              disabled={isLoading}
            />
            {errors.alpacaApiKey && (
              <p className="mt-1 text-sm text-red-500">{errors.alpacaApiKey}</p>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Alpaca Secret Key
            </label>
            <Input
              type="password"
              placeholder="Enter your secret key"
              value={keys.alpacaSecretKey}
              onChange={(e) => handleKeyChange("alpacaSecretKey", e.target.value)}
              className={`bg-black/30 border-yellow-500/30 text-white ${errors.alpacaSecretKey ? "border-red-500" : ""}`}
              disabled={isLoading}
            />
            {errors.alpacaSecretKey && (
              <p className="mt-1 text-sm text-red-500">{errors.alpacaSecretKey}</p>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Alpaca Endpoint
            </label>
            <Input
              type="text"
              value={keys.alpacaEndpoint}
              onChange={(e) => handleKeyChange("alpacaEndpoint", e.target.value)}
              className="bg-black/30 border-yellow-500/30 text-white"
              disabled={isLoading}
            />
          </div>
        </div>
      </div>

      <div className="flex gap-4 mt-8">
        <Button 
          onClick={handleSave}
          className="bg-yellow-500 hover:bg-yellow-600 text-black"
          disabled={Object.values(errors).some(error => error !== "") || isLoading}
        >
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin mr-2" />
          ) : null}
          Save Keys
        </Button>
      </div>
    </div>
  );
} 