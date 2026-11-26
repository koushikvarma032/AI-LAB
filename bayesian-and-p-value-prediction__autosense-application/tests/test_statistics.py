import pytest
from services.statistical_service import StatisticalEngine
from config import Config

def test_statistical_engine_initialization():
    engine = StatisticalEngine()
    assert engine.df is not None
    assert len(engine.df) > 0
    assert engine.alpha == Config.ALPHA

def test_run_all_variable_tests():
    engine = StatisticalEngine()
    results = engine.run_all_variable_tests(target_fault='BATTERY_FAILURE')
    assert isinstance(results, list)
    assert len(results) >= 11 # 6 continuous + 5 symptoms
    
    for item in results:
        assert 'variable' in item
        assert 'statistic' in item
        assert 'p_value' in item
        assert 0.0 <= item['p_value'] <= 1.0
        assert item['alpha'] == 0.05
        assert isinstance(item['is_significant'], (bool, type(True), type(False)))
