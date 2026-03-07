import * as React from "react"

const Badge = React.forwardRef(({ className, variant = "default", ...props }, ref) => {
  const variants = {
    default: "bg-surface-elevated text-subtle-foreground border-border",
    accent: "bg-accent/5 text-accent border-accent/10",
  }

  return (
    <div
      ref={ref}
      className={`inline-flex items-center rounded border px-2 py-1 text-12 font-normal uppercase tracking-wide transition-colors ${variants[variant]} ${className || ''}`}
      {...props}
    />
  )
})
Badge.displayName = "Badge"

export { Badge }
