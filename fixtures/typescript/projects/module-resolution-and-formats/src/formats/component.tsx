export interface PanelProps {
  title: string;
  count: number;
}

export function Panel(props: PanelProps): JSX.Element {
  return <section title={props.title}>{props.count}</section>;
}

export const panelJsx = <Panel title="demo" count={1} />;

export const panelTag = "panel";
