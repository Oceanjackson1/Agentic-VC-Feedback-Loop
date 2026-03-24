"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { googleLogin } from "@/lib/api";
import { Suspense } from "react";

function LoginHandler() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const code = searchParams.get("code");
    if (!code) {
      router.push("/");
      return;
    }

    const redirectUri = `${window.location.origin}/login`;

    googleLogin(code, redirectUri)
      .then((data) => {
        login(data.token, data.user);
        router.push("/dashboard");
      })
      .catch((err) => {
        setError(err.message || "登录失败");
      });
  }, [searchParams, router, login]);

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4">
        <div className="px-4 py-3 rounded-xl bg-error-light text-error text-sm">
          {error}
        </div>
        <button
          onClick={() => router.push("/")}
          className="text-sm text-accent hover:underline"
        >
          返回首页
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex items-center gap-3 text-text-secondary">
        <div className="w-5 h-5 border-2 border-border-strong border-t-accent rounded-full animate-spin-slow" />
        正在登录...
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center">
          <div className="w-6 h-6 border-2 border-border-strong border-t-accent rounded-full animate-spin-slow" />
        </div>
      }
    >
      <LoginHandler />
    </Suspense>
  );
}
