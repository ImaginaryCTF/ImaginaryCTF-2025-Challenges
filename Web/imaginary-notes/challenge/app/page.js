"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { supabase } from "./supabase"

export default function AuthPage() {
  const router = useRouter()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  async function handleLogin(e) {
    e.preventDefault()
    setError("")

    const { data, error: queryError } = await supabase
      .from("users")
      .select("*")
      .eq("username", username)
      .eq("password", password) // ⚠️ plaintext password = CTF-vulnerable!
      .single()

    if (queryError || !data) {
      setError("Invalid username or password")
    } else {
      localStorage.setItem("username", username)
      router.push("/notes")
    }
  }

  async function handleSignup(e) {
    e.preventDefault()
    setError("")

    const { data: existing } = await supabase
      .from("users")
      .select("id")
      .eq("username", username)
      .maybeSingle()

    if (existing) {
      setError("Username already exists")
      return
    }

    const { error: insertError } = await supabase.from("users").insert([
      { username, password }, // ⚠️ Plaintext password again (CTF-acceptable)
    ])

    if (insertError) {
      setError("Signup failed: " + insertError.message)
    } else {
      localStorage.setItem("username", username)
      router.push("/notes")
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <form className="max-w-sm w-full space-y-4">
        <h1 className="text-2xl font-bold">Login / Signup</h1>

        <input
          type="text"
          placeholder="Username"
          className="w-full border p-2 rounded"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border p-2 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div className="flex gap-4">
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
            onClick={handleLogin}
          >
            Log In
          </button>
          <button
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 w-full"
            onClick={handleSignup}
          >
            Sign Up
          </button>
        </div>

        {error && <p className="text-red-500 text-sm">{error}</p>}
      </form>
    </main>
  )
}
