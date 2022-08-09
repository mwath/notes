export default function slugify(text: string): string {
  return text
    .toString()
    .normalize("NFKD")
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/([^\w\-]+|(?<=\-)\-)/g, "")
    .replace(/(^\-+|\-+$)/g, "");
}
