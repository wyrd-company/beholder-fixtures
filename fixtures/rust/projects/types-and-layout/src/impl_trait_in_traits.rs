//! RS-CAN-TYPE-011 — RPIT and `async fn` in traits.

use std::future::Future;

// Trait returning an opaque iterator; each impl chooses its own hidden type.
pub trait PlotSource {
    fn plots(&self) -> impl Iterator<Item = String>;
    fn count(&self) -> usize
    where
        Self: Sized;
}

// Trait with async method; each impl chooses different future shape.
pub trait Harvest {
    fn harvest(&self) -> impl Future<Output = String> + Send;
}

pub struct Field {
    pub rows: Vec<String>,
}

pub struct Garden {
    pub beds: Vec<String>,
}

impl PlotSource for Field {
    fn plots(&self) -> impl Iterator<Item = String> {
        self.rows.clone().into_iter()
    }

    fn count(&self) -> usize {
        self.rows.len()
    }
}

impl PlotSource for Garden {
    fn plots(&self) -> impl Iterator<Item = String> {
        // Different hidden type: map adapter chain differs from Field.
        self.beds.iter().map(|b| format!("garden-{b}"))
    }

    fn count(&self) -> usize {
        self.beds.len()
    }
}

impl Harvest for Field {
    fn harvest(&self) -> impl Future<Output = String> + Send {
        let total = self.rows.len();
        async move { format!("field {total}") }
    }
}

impl Harvest for Garden {
    fn harvest(&self) -> impl Future<Output = String> + Send {
        // Different hidden future due to extra await point.
        let total = self.beds.len();
        async move {
            let label = async { total }.await;
            format!("garden {label}")
        }
    }
}

// Native async fn in trait.
#[allow(async_fn_in_trait)]
pub trait AsyncPlot {
    async fn plot_name(&self) -> String;
}

pub struct Meadow {
    pub label: String,
}

pub struct Orchard {
    pub trees: usize,
}

impl AsyncPlot for Meadow {
    async fn plot_name(&self) -> String {
        self.label.clone()
    }
}

impl AsyncPlot for Orchard {
    async fn plot_name(&self) -> String {
        format!("orchard-{}", self.trees)
    }
}

// Boxed-future object-safe form for comparison.
pub trait BoxedPlot: Send + Sync {
    fn plot_name_boxed(&self) -> std::pin::Pin<Box<dyn Future<Output = String> + Send + '_>>;
}

impl BoxedPlot for Meadow {
    fn plot_name_boxed(&self) -> std::pin::Pin<Box<dyn Future<Output = String> + Send + '_>> {
        let owned = self.label.clone();
        Box::pin(async move { owned })
    }
}

impl BoxedPlot for Orchard {
    fn plot_name_boxed(&self) -> std::pin::Pin<Box<dyn Future<Output = String> + Send + '_>> {
        let n = self.trees;
        Box::pin(async move { format!("orchard-{n}") })
    }
}

pub fn generic_calls<T: PlotSource>(source: &T) -> Vec<String> {
    source.plots().collect()
}

pub async fn harvest_all<H: Harvest>(source: &H) -> String {
    source.harvest().await
}

pub async fn async_trait_calls<A: AsyncPlot>(source: &A) -> String {
    source.plot_name().await
}

pub fn boxed_calls(
    item: &dyn BoxedPlot,
) -> std::pin::Pin<Box<dyn Future<Output = String> + Send + '_>> {
    item.plot_name_boxed()
}
