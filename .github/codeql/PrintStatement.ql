/**
 * @name Using Print Statement in Production Code
 * @description Using Print Statement in Production Code
 * @kind problem
 * @problem.severity recommendation
 * @id py/print-statement
 * @precision very-high
 * @tags correctness
 */

import python
import semmle.python.Concepts
import semmle.python.ApiGraphs
import semmle.python.dataflow.new.DataFlow

from DataFlow::Node print
where print = API::builtin("print").getACall()
select print, "use of print statement"

