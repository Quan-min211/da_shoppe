# ==============================
# Frontend Dockerfile — Next.js
# ==============================
# Multi-stage build: build → chỉ deploy output tĩnh

FROM node:20-alpine AS base

# ---- Stage 1: Dependencies ----
FROM base AS deps

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci 2>/dev/null || npm install

# ---- Stage 2: Build ----
FROM base AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build-time env: API URL trỏ vào Docker service name
ENV NEXT_PUBLIC_API_URL=http://backend:8000
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# ---- Stage 3: Runtime ----
FROM base AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Tạo user non-root
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy built output
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:3000/ || exit 1

CMD ["node", "server.js"]
