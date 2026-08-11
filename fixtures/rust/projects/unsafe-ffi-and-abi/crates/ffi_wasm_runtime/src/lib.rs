//! RS-CAN-PROJ-017 freestanding wasm runtime hooks, target-gated.

#![no_std]

#[cfg(target_arch = "wasm32")]
mod wasm_hooks {
    use core::alloc::{GlobalAlloc, Layout};
    use core::panic::PanicInfo;

    struct BumpAllocator;

    unsafe impl GlobalAlloc for BumpAllocator {
        unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
            if layout.size() == 0 {
                layout.align() as *mut u8
            } else {
                core::ptr::null_mut()
            }
        }
        unsafe fn dealloc(&self, _ptr: *mut u8, _layout: Layout) {}
    }

    #[global_allocator]
    static ALLOCATOR: BumpAllocator = BumpAllocator;

    #[panic_handler]
    fn panic(_info: &PanicInfo) -> ! {
        core::arch::wasm32::unreachable()
    }

    #[unsafe(no_mangle)]
    pub extern "C" fn _start() {
        core::hint::black_box(0);
    }
}

#[cfg(target_arch = "wasm32")]
pub use wasm_hooks::_start;

/// Marker for the wasm entry symbol name.
pub fn wasm_entry_name() -> &'static str {
    if cfg!(target_arch = "wasm32") {
        "_start"
    } else {
        "host"
    }
}
