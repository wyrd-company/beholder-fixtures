# typed-toolkit-partial (runtime)

Matching runtime distribution for the partial stub overlay.  Provides package
`partial_pkg` with an inline-types `py.typed` marker.  The separate
`typed-toolkit-partial-stubs` distribution overlays a *partial* `partial_pkg-stubs`
package: symbols it omits fall back to this package's inline types.
