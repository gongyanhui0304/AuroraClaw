export function LangGraphLogoSVG({
  className,
  width,
  height,
}: {
  width?: number;
  height?: number;
  className?: string;
}) {
  return (
  <img
    src="/通明灵犀logo.svg"
    alt="通明灵犀"
    className={className}
    width={width}
    height={height}
  />
);
}