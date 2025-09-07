"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

export default function NotesPage() {
  const router = useRouter()
  const [note, setNote] = useState("")
  const [notes, setNotes] = useState([])
  const [username, setUsername] = useState("")

  useEffect(() => {
    const user = localStorage.getItem("username")
    if (!user) {
      router.push("/")
    } else {
      setUsername(user)
    }
  }, [router])

  function addNote() {
    if (!note.trim()) return
    setNotes([...notes, note.trim()])
    setNote("")
  }

  function logout() {
    localStorage.removeItem("username")
    router.push("/")
  }

  return (
    <main className="max-w-xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Welcome, {username}</h1>

      <textarea
        className="w-full border rounded p-2 mb-2"
        rows={4}
        placeholder="Write a note..."
        value={note}
        onChange={(e) => setNote(e.target.value)}
      />

      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={addNote}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Add Note
        </button>
        <button
          onClick={logout}
          className="text-sm text-gray-600 underline hover:text-gray-800"
        >
          Logout
        </button>
      </div>

      <section>
        <h2 className="text-xl font-semibold mb-2">Your Notes</h2>
        {notes.length === 0 && <p className="text-gray-500">No notes yet.</p>}
        <ul className="space-y-2">
          {notes.map((n, i) => (
            <li key={i} className="border p-2 rounded bg-gray-100">
              {n}
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
