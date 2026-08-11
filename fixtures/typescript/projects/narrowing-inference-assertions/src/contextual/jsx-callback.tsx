// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

type PanelProps = {
  label: string;
  onSelect: (value: string) => void;
  children?: string;
};

function Panel(props: PanelProps): JSX.Element {
  void props;
  return { _jsxBrand: `panel:${props.label}` };
}

export function jsxCallbackWithContext(): JSX.Element {
  const element = (
    <Panel label="atlas" onSelect={(value) => void value.toUpperCase()} />
  );
  return element;
}

export function jsxCallbackWithoutContext(): JSX.Element {
  const handler = (value: string): void => {
    void value.toUpperCase();
  };
  const element = <Panel label="ledger" onSelect={handler} />;
  return element;
}

export function jsxCallbackContextContrast(): [JSX.Element, JSX.Element] {
  const withContext = (
    <Panel label="atlas" onSelect={(value) => void value.length} />
  );
  const localHandler: (value: string) => void = (value) => void value.length;
  const withoutContext = <Panel label="ledger" onSelect={localHandler} />;
  return [withContext, withoutContext];
}
