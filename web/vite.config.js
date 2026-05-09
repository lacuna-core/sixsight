import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// On GitHub Pages the site lives at /<repo-name>/; locally it's at /.
// GITHUB_REPOSITORY is set automatically by Actions as "owner/repo".
const base = process.env.GITHUB_REPOSITORY
  ? `/${process.env.GITHUB_REPOSITORY.split('/')[1]}/`
  : '/'

export default defineConfig({
  plugins: [react()],
  base,
})
