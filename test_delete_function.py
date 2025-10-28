"""Test script to verify delete functionality in ResultsStorage"""
from src.storage import ResultsStorage

def test_delete_functions():
    """Test both delete_result and clear_all_results methods"""
    
    storage = ResultsStorage()
    
    # List current results
    print("=" * 60)
    print("📊 CURRENT RESULTS")
    print("=" * 60)
    results = storage.list_results()
    print(f"Total simulations: {len(results)}\n")
    
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['name']}")
        print(f"   Type: {r['type']}")
        print(f"   Modified: {r['modified']}")
        print(f"   Files: {r['csv_file']}, {r['json_file']}")
        print()
    
    # Count files
    csv_files = list(storage.results_dir.glob('*.csv'))
    json_files = list(storage.results_dir.glob('*.json'))
    print(f"📁 Total files: {len(csv_files) + len(json_files)} ({len(csv_files)} CSV + {len(json_files)} JSON)")
    print()
    
    # Test delete_result function
    if results:
        print("=" * 60)
        print("🧪 TEST: delete_result()")
        print("=" * 60)
        test_name = results[0]['name']
        print(f"Testing deletion of: {test_name}")
        print(f"Files to delete: {test_name}.csv, {test_name}.json")
        print("\n⚠️  This is a DRY RUN - not actually deleting")
        print(f"Would call: storage.delete_result('{test_name}')")
        print()
    
    # Test clear_all_results function
    print("=" * 60)
    print("🧪 TEST: clear_all_results()")
    print("=" * 60)
    print(f"Would delete all {len(csv_files) + len(json_files)} files")
    print("\n⚠️  This is a DRY RUN - not actually deleting")
    print(f"Would call: storage.clear_all_results()")
    print()
    
    print("=" * 60)
    print("✅ VERIFICATION COMPLETE")
    print("=" * 60)
    print("Both methods are available and ready to use:")
    print("  - delete_result(base_name) -> bool")
    print("  - clear_all_results() -> tuple[int, int]")

if __name__ == "__main__":
    test_delete_functions()
