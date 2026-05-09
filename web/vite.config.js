import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { existsSync } from 'fs'

// A CNAME file means a custom domain is active — the site lives at the root.
// Without one, fall back to /<repo-name>/ for GitHub Pages subpath hosting.
const hasCname = existsSync('./public/CNAME')
const base = hasCname
  ? '/'
  : process.env.GITHUB_REPOSITORY
    ? `/${process.env.GITHUB_REPOSITORY.split('/')[1]}/`
    : '/'

export default defineConfig({
  plugins: [react()],
  base,
})
