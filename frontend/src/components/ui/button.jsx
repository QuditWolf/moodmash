import * as React from "react"

const Button = React.forwardRef(({ className, variant = "default", size = "default", ...props }, ref) => {
  const variants = {
    default: "bg-surface text-foreground hover:bg-surface-elevated border border-border",
    ghost: "hover:bg-surface/50 hover:text-foreground",
    link: "text-muted-foreground hover:text-foreground",
  }

  const sizes = {
    default: "h-9 px-4 py-2",
    sm: "h-8 px-3 text-12",
    lg: "h-10 px-5",
    icon: "h-9 w-9",
  }

  return (
    <button
      className={`inline-flex items-center justify-center rounded-md text-14 font-normal transition-all duration-180 ease-premium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent/30 disabled:pointer-events-none disabled:opacity-40 ${variants[variant]} ${sizes[size]} ${className || ''}`}
      ref={ref}
      {...props}
    />
  )
})
Button.displayName = "Button"

export { Button }
