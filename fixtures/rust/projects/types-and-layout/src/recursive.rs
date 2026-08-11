//! RS-CAN-TYPE-012 — boxed and mutually recursive types via indirection.

#[derive(Debug, PartialEq, Default)]
pub enum List {
    Cons(i32, Box<List>),
    #[default]
    Nil,
}

impl List {
    #[allow(clippy::new_without_default)]
    pub fn new() -> Self {
        List::Nil
    }

    pub fn prepend(self, value: i32) -> Self {
        List::Cons(value, Box::new(self))
    }

    #[allow(clippy::len_without_is_empty)]
    pub fn len(&self) -> usize {
        match self {
            List::Nil => 0,
            List::Cons(_, rest) => 1 + rest.len(),
        }
    }

    pub fn is_empty(&self) -> bool {
        matches!(self, List::Nil)
    }
}

#[derive(Debug, PartialEq)]
pub struct Tree {
    pub value: i32,
    pub left: Option<Box<Tree>>,
    pub right: Option<Box<Tree>>,
}

impl Tree {
    pub fn leaf(value: i32) -> Self {
        Self {
            value,
            left: None,
            right: None,
        }
    }

    pub fn with_children(value: i32, left: Tree, right: Tree) -> Self {
        Self {
            value,
            left: Some(Box::new(left)),
            right: Some(Box::new(right)),
        }
    }
}

// Mutually recursive types through indirection.
#[derive(Debug, PartialEq)]
pub struct Branch {
    pub leaf: Option<Box<Leaf>>,
}

#[derive(Debug, PartialEq)]
pub struct Leaf {
    pub branches: Vec<Branch>,
}

// DST recursion via boxed trait object.
pub trait Node: std::fmt::Debug {
    fn weight(&self) -> i32;
}

#[derive(Debug)]
pub struct Weighted {
    pub weight: i32,
    pub child: Option<Box<dyn Node>>,
}

impl Node for Weighted {
    fn weight(&self) -> i32 {
        self.weight + self.child.as_ref().map(|c| c.weight()).unwrap_or(0)
    }
}

pub fn recursive_examples() {
    let list = List::Nil.prepend(3).prepend(2).prepend(1);
    assert_eq!(list.len(), 3);

    let tree = Tree::with_children(1, Tree::leaf(2), Tree::leaf(3));
    assert_eq!(tree.value, 1);

    let branch = Branch {
        leaf: Some(Box::new(Leaf {
            branches: vec![Branch { leaf: None }],
        })),
    };
    assert!(branch.leaf.is_some());
}

pub fn dst_recursive_example() -> Box<dyn Node> {
    let leaf: Box<dyn Node> = Box::new(Weighted {
        weight: 2,
        child: None,
    });
    Box::new(Weighted {
        weight: 5,
        child: Some(leaf),
    })
}
