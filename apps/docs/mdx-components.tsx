import type { MDXComponents } from "mdx/types";
import Image, { ImageProps } from "next/image";

const components: MDXComponents = {
  img: (props) => (
    <div className="my-6">
      <Image
        sizes="100vw"
        width={800}
        height={450}
        className="rounded-lg border border-white/10"
        style={{ width: "100%", height: "auto" }}
        {...(props as ImageProps)}
        alt={props.alt || "MDX Image"}
      />
    </div>
  ),
};

export function useMDXComponents(
  providedComponents: MDXComponents,
): MDXComponents {
  return {
    ...providedComponents,
    ...components,
  };
}
