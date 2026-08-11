export interface PanelProps {
  title: string;
  count: number;
}

export function Panel(props: PanelProps): string {
  return `<panel title="${props.title}" count="${props.count}" />`;
}

export const panelTag = "panel";
